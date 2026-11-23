"""Public, read-only MOKE MCP fallback; standard library only, no credentials.

Prefer connected MCP tools. This helper never logs in, installs skills, executes
returned files, uploads prompts, or calls a generation model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import PurePosixPath
import sys
import urllib.error
import urllib.request

ENDPOINT = 'https://www.mokeaigc.ai/mcp'
PROTOCOL = '2025-03-26'
MAX_RESPONSE = 4 * 1024 * 1024


class MCPError(RuntimeError):
    pass


def same_request_id(value, expected):
    # Python bool subclasses int, but JSON true is not the request number 1.
    return not isinstance(value, bool) and not isinstance(expected, bool) and value == expected


def decode_response(body: bytes, content_type: str, request_id):
    if 'text/event-stream' in content_type:
        candidates = []
        data_lines = []
        for line in body.decode('utf-8-sig').splitlines() + ['']:
            if not line:
                if data_lines:
                    candidates.append(json.loads('\n'.join(data_lines)))
                    data_lines = []
            elif line.startswith('data:'):
                data_lines.append(line[5:].lstrip(' '))
        matches = [item for item in candidates if isinstance(item, dict) and same_request_id(item.get('id'), request_id)]
        if len(matches) != 1:
            raise MCPError('Expected one matching JSON-RPC response in SSE.')
        result = matches[0]
    else:
        result = json.loads(body.decode('utf-8-sig'))
    if not isinstance(result, dict) or result.get('jsonrpc') != '2.0' or not same_request_id(result.get('id'), request_id):
        raise MCPError('Unexpected JSON-RPC response identity.')
    if 'error' in result:
        raise MCPError(json.dumps(result['error'], ensure_ascii=False))
    if 'result' not in result:
        raise MCPError('Missing JSON-RPC result.')
    return result['result']


def tool_data(result):
    if not isinstance(result, dict):
        raise MCPError('Unexpected MCP tool result.')
    if result.get('isError'):
        value = result.get('structuredContent') or result.get('content') or 'MOKE tool failed.'
        raise MCPError(json.dumps(value, ensure_ascii=False))
    if 'structuredContent' in result:
        if not isinstance(result['structuredContent'], dict):
            raise MCPError('Expected structured material object.')
        return result['structuredContent']
    content = result.get('content', [])
    if not isinstance(content, list) or any(not isinstance(x, dict) for x in content):
        raise MCPError('Expected MCP content blocks as objects.')
    blocks = [x.get('text') for x in content if x.get('type') == 'text']
    if len(blocks) != 1:
        raise MCPError('Expected structured material data or one JSON text block.')
    if not isinstance(blocks[0], str):
        raise MCPError('Expected one JSON text block.')
    parsed = json.loads(blocks[0])
    if not isinstance(parsed, dict):
        raise MCPError('Expected a material object in the JSON text block.')
    return parsed


class Client:
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session_id = None
        self.protocol = PROTOCOL
        self.sequence = 0

    def request(self, method, params=None, notification=False):
        self.sequence += 1
        request_id = self.sequence
        payload = {'jsonrpc': '2.0', 'method': method}
        if not notification:
            payload['id'] = request_id
        if params is not None:
            payload['params'] = params
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json, text/event-stream',
                   'MCP-Protocol-Version': self.protocol}
        if self.session_id:
            headers['Mcp-Session-Id'] = self.session_id
        req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode('utf-8'),
                                     headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.headers.get('mcp-session-id'):
                    self.session_id = response.headers['mcp-session-id']
                if notification:
                    return None
                body = response.read(MAX_RESPONSE + 1)
                if len(body) > MAX_RESPONSE:
                    raise MCPError('MOKE response exceeds the supported size.')
                return decode_response(body, response.headers.get('content-type', ''), request_id)
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise MCPError('Public access denied. Use the authenticated MOKE connector for this material.') from exc
            raise MCPError(f'MOKE HTTP {exc.code}; no automatic retry performed.') from exc

    def initialize(self):
        result = self.request('initialize', {'protocolVersion': PROTOCOL, 'capabilities': {},
                                            'clientInfo': {'name': 'an-workflow-public-reader', 'version': '1.0'}})
        self.protocol = result['protocolVersion']
        self.request('notifications/initialized', notification=True)
        return {'serverInfo': result.get('serverInfo'), 'protocolVersion': self.protocol,
                'access': 'public_noauth'}

    def call(self, name, arguments):
        return tool_data(self.request('tools/call', {'name': name, 'arguments': arguments}))


def verified_read(client, material_id, version, path, language='zh'):
    parsed = PurePosixPath(path)
    if not path or '\\' in path or parsed.is_absolute() or '..' in parsed.parts or ':' in path:
        raise MCPError('Use an exact relative path from get_material.files.')
    arguments = {'id': material_id, 'version': version, 'language': language}
    detail = client.call('get_material', arguments)
    if detail.get('id') != material_id or detail.get('version') != version:
        raise MCPError('Material identity/version changed; restart the search.')
    files = detail.get('files', [])
    if not isinstance(files, list) or any(not isinstance(item, dict) for item in files):
        raise MCPError('Expected material files as objects.')
    matches = [item for item in files if item.get('path') == path]
    if len(matches) != 1 or not matches[0].get('sha256'):
        raise MCPError('Path is not listed with a SHA-256 in this material version.')
    result = client.call('read_skill_file', {**arguments, 'path': path})
    if (result.get('id'), result.get('version'), result.get('path')) != (material_id, version, path):
        raise MCPError('Returned file does not match the requested material/version/path.')
    text = result.get('text')
    if not isinstance(text, str):
        raise MCPError('Returned file has no UTF-8 text.')
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    if digest != matches[0]['sha256'] or result.get('sha256') != digest:
        raise MCPError('File hash mismatch; do not adopt this content. Restart the search.')
    return {**result, 'verified_sha256': True}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('tools', help='Initialize and list currently advertised public MCP tools.')
    search = sub.add_parser('search', help='Search summaries; omittedTypes must remain visible.')
    search.add_argument('query')
    search.add_argument('--type', choices=['all', 'skill', 'prompt'], default='skill')
    search.add_argument('--category')
    search.add_argument('--language', choices=['zh', 'en'], default='zh')
    search.add_argument('--limit', type=int, choices=range(1, 51), default=5)
    search.add_argument('--cursor')
    for command in ['get', 'read']:
        item = sub.add_parser(command)
        item.add_argument('--id', required=True)
        item.add_argument('--version', required=True)
        item.add_argument('--language', choices=['zh', 'en'], default='zh')
        if command == 'read':
            item.add_argument('--path', required=True)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        client = Client()
        connection = client.initialize()
        if args.command == 'tools':
            result = {**connection, **client.request('tools/list', {})}
        elif args.command == 'search':
            arguments = {'query': args.query, 'type': args.type, 'language': args.language, 'limit': args.limit}
            if args.category is not None:
                arguments['category'] = args.category
            if args.cursor is not None:
                arguments['cursor'] = args.cursor
            result = client.call('search_materials', arguments)
        elif args.command == 'get':
            result = client.call('get_material', {'id': args.id, 'version': args.version, 'language': args.language})
        else:
            result = verified_read(client, args.id, args.version, args.path, args.language)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (MCPError, urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc), 'access': 'public_noauth', 'retry': 'none'}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
