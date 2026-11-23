"""Text hygiene and optional explicit 2-D geometry checks; not a video verifier.

Exit 0: enumerated checks passed, 1: detected errors, 2: invalid invocation/input.
Geometry JSON: projections[{camera,look_at,subject,facing?,screen?,view?}],
routes[{points,obstacles:[{min,max}]}], axes[{a,b,cameras,bridge?}],
distances[{a,b,min?,max?,claimed?,tolerance?}],
motions[{from,to,facing?,direction?,target_from?,target_to?,distance_change?,duration?,max_speed?}],
dynamic_axes[{frames:[{a,b,camera}],bridge?}].
Coordinates are [east,north]. Geometry is supplied evidence, not parsed prose.
"""
import argparse
import json
import math
import re
from pathlib import Path

# Shot envelopes and body intervals are separate timelines, never summed.
NUMBER = r'-?\d+(?:\.\d+)?'
INTERVAL = rf'({NUMBER})\s*(?:s|秒)?\s*[-—–~～至]\s*({NUMBER})\s*(?:秒|s)'
TIME = re.compile(rf'^\s*(?:[【\[])?(?:S\s*=\s*)?{INTERVAL}', re.I)
SHOT = re.compile(r'^\s*(?:[【\[])?镜头\s*\d*\s*[：:]\s*(?:S\s*=\s*)?', re.I)
RANGE = re.compile(INTERVAL, re.I)
EVENT = re.compile(rf'(?<![A-Za-z0-9_])t\s*=\s*({NUMBER})(?![\d.eE])\s*(?:s|秒)?', re.I)
QUOTED = re.compile(r'“[^”]*”|「[^」]*」|『[^』]*』|"(?:\\.|[^"\\])*"')
FIELD = re.compile(r'^\s*(fx-env|sound|transition)\s*[：:]\s*(.*)', re.I)


def finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def load_input_json(path):
    """Reject repeated constraint/contract keys rather than silently dropping one."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('JSON存在重复字段: ' + key)
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError('JSON不接受非有限数: ' + value)
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique,
                      parse_constant=invalid_constant)


def mask_speech_literals(text, contract):
    """Keep spoken literal tokens out of directive-only hygiene checks.

    Limit the exemption to documented, single-line sound dialogue: an explicit
    speech marker or a speaker from the original dialogue contract. Quoted asset
    references in visual instructions or music references remain directives.
    """
    masked = list(text)
    speakers = [item['speaker'] for item in (contract or {}).get('dialogue', [])]
    for field in re.finditer(r'^[ \t]*sound[ \t]*[：:][ \t]*(.*)', text, re.M | re.I):
        value = field[1]
        previous = 0
        for quote in QUOTED.finditer(value):
            prefix = value[previous:quote.start()].strip()
            speech = re.search(r'对白|台词|旁白|念出|读出|朗读|dialogue|voice.?over', prefix, re.I)
            known_speaker = any(re.match(re.escape(s) + r'(?=\s|[，,:：、（(]|$)', prefix) for s in speakers)
            if speech or known_speaker:
                start = field.start(1) + quote.start()
                end = field.start(1) + quote.end()
                masked[start:end] = ['\n' if c == '\n' else ' ' for c in text[start:end]]
            previous = quote.end()
    return ''.join(masked)


def mask_quotes(text):
    """Keep offsets and newlines while excluding literal spoken/quoted text."""
    return QUOTED.sub(lambda m: ''.join('\n' if c == '\n' else ' ' for c in m.group()), text)


def check_event_times(text, blocks, add):
    """Explicit absolute anchors only; numerical scope/order, never motion feasibility."""
    masked = mask_quotes(text)
    covered = set()
    for block in blocks:
        where = block['span'][2]
        body = masked[where:where + len(''.join(block['lines']))]
        left, right = block['span'][:2]
        first_field = re.search(r'^\s*(?:fx-env|sound|transition)\s*[：:]', body, re.M | re.I)
        action_end = first_field.start() if first_field else len(body)
        previous = None
        for match in EVENT.finditer(body):
            at = where + match.start()
            covered.add(at)
            value = float(match[1])
            if not math.isfinite(value) or value < left-1e-6 or value > right+1e-6:
                add('EVENT_TIME_RANGE', f'绝对事件时间{match[1]}不在所属S段{left}–{right}内', at)
            if match.start() < action_end:
                if previous is not None and value < previous-1e-6:
                    add('EVENT_TIME_ORDER', '行动段内绝对t=节点的书写顺序回退；引用/倒叙应另行人工核对', at)
                previous = value
    numeric_starts = set()
    for match in EVENT.finditer(masked):
        numeric_starts.add(match.start())
        if match.start() not in covered:
            add('EVENT_SCOPE_REVIEW', '数值t=未归属可解析S正文，需人工确认范围', match.start(), 'review')
    for match in re.finditer(r'(?<![A-Za-z0-9_])t\s*=', masked, re.I):
        if match.start() not in numeric_starts:
            add('EVENT_SYNTAX_REVIEW', '无法按普通数字解析t=；相对、引用或其他语法需人工核对', match.start(), 'review')
    for match in re.finditer(r'(?<![A-Za-z0-9_])t\s*≈', masked, re.I):
        add('EVENT_APPROX_REVIEW', '近似t≈不按精确绝对锚点验收', match.start(), 'review')


def check_text(text, duration=None, references=(), allow_platform_params=False,
               *, start=0, end=None, profile='basic', contract=None, event_times='review'):
    """Basic API preserves legacy hygiene calls; fusion enables the fixed template.

    duration is the legacy absolute end, NOT the length of a continuation.
    contract dialogue is a list of {speaker,text} in utterance order.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError('正文不能为空')
    if profile not in {'basic', 'fusion', 'compact', 'prose'}:
        raise ValueError('profile仅支持basic/fusion/compact/prose')
    if event_times not in {'review', 'absolute'}:
        raise ValueError('event_times仅支持review/absolute')
    if not finite_number(start) or start < 0:
        raise ValueError('start必须为有限非负数')
    if duration is not None and (not finite_number(duration) or duration <= 0):
        raise ValueError('duration必须为有限正数')
    if end is not None and (not finite_number(end) or end <= start):
        raise ValueError('end必须为大于start的有限数')
    if duration is not None and end is not None and abs(duration-end) > 1e-6:
        raise ValueError('旧参数duration与end冲突；两者都表示绝对终点')
    target_end = end if end is not None else duration
    if target_end is not None and target_end <= start:
        raise ValueError('绝对终点必须大于start')
    validate_contract(contract)
    directives = mask_speech_literals(text, contract)
    issues = []
    def add(code, message, start=0, severity='error'):
        issues.append(dict(code=code, severity=severity,
                           line=text.count('\n', 0, start) + 1, message=message))
    patterns = [
        ('CITATION_LEAK', r'\[cite\s*:\s*[^\]]+\]|[^]*', '删除来源脚注/工具引用'),
        ('TEMPLATE_SLOT', r'\{\{[^}]+\}\}|\[(?:主体|角色名称|待填|PLACEHOLDER|TODO)\]|<\|[^>]+\|>', '未填模板或控制词元'),
        ('CONTEXT_LEAK', r'本段是项目第|arvin_v1_checks|Resolved Policy', '后台字段混入正文'),
        ('CONTROL_CHAR', r'[\x00-\x08\x0b\x0c\x0e-\x1f\ufffd]', '异常控制字符或解码替代符'),
    ]
    if not allow_platform_params:
        patterns.append(('PLATFORM_TOKEN', r'--(?:ar|stylize|profile|chaos|seed)\b', '疑似其他平台命令；确认目标支持后才保留'))
    for code, pattern, message in patterns:
        scanned = directives if code in {'PLATFORM_TOKEN','TEMPLATE_SLOT','CONTEXT_LEAK'} else text
        for match in re.finditer(pattern, scanned):
            add(code, message, match.start())
    for match in re.finditer(r'@(?:图片|视频|音频|image|video|audio)\d+', directives, re.I):
        if match.group() not in references:
            add('UNBOUND_REFERENCE', '素材标签未在本次实际素材清单中绑定: ' + match.group(), match.start())

    for match in re.finditer(r'如上所述|同上|按上文', text):
        add('CONTEXT_REVIEW', '核对是否引用生成端不可见内容；台词或同份文本中的明确引用不自动判错', match.start(), 'review')

    spans, shots, shot_bodies, shot_offsets, blocks = [], [], [], [], []
    shot_labels, dissolve_targets = [], {}
    # Register all headers, including untimed black/title-card headers.
    dissolves = {}
    current_block = None
    offset = 0
    for line in text.splitlines(keepends=True):
        header = SHOT.match(line)
        if header:
            tail = line[header.end():]
            card = re.match(r'(?:黑场|字幕卡)\s*(?:S\s*=\s*)?', tail)
            match = RANGE.match(tail, card.end() if card else 0)
            if not match and not card and profile == 'fusion':
                add('SHOT_TIME_MISSING', '普通镜头头部缺少可解析时间窗', offset)
        else:
            match = TIME.match(line)
        if header:
            shots.append(None)
            shot_bodies.append([])
            shot_offsets.append(offset)
            label = re.search(r'镜头\s*(\d*)\s*[：:]', line)[1]
            shot_labels.append(label or str(len(shots)))
            current_block = None
        if match:
            left, right = map(float, match.groups())
            span = (left, right, offset)
            if header:
                shots[-1] = span
            else:
                spans.append(span)
                if shots:
                    shot_bodies[-1].append(span)
                current_block = {'span': span, 'fields': {}, 'lines': [],
                                 'shot': len(shots)-1}
                blocks.append(current_block)
        elif re.match(r'^\s*(?:[【\[])?S\s*=', line, re.I) or (header and re.search(r'S\s*=', line, re.I)):
            add('TIME_SYNTAX', '无法解析显式S=时间窗；使用数字起止与秒单位', offset)
        if current_block is not None and not header:
            current_block['lines'].append(line)
            field = FIELD.match(line)
            if field:
                key = field[1].lower()
                current_block['fields'].setdefault(key, []).append((field[2].strip(), offset))
        if re.match(r'^\s*transition\s*[：:]\s*叠化\b', line):
            declared = re.search(rf'叠化\s+S\s*=\s*{INTERVAL}', line)
            if declared and shots:
                if len(shots)-1 in dissolves:
                    add('DISSOLVE_SYNTAX', '一个镜间衔接只能声明一个叠化区间', offset)
                dissolves[len(shots)-1] = (*map(float, declared.groups()), offset)
                target = re.search(r'镜头\s*(\d+)\s*→\s*镜头\s*(\d+)', line)
                adjacent = re.search(r'(?:前镜|当前镜)\s*→\s*(?:后镜|下一镜)', line)
                dissolve_targets[len(shots)-1] = target.groups() if target else 'adjacent' if adjacent else None
            else:
                add('DISSOLVE_SYNTAX', '使用transition：叠化 S=起–止s；前镜→后镜', offset)
        offset += len(line)

    for i, (shot, body) in enumerate(zip(shots, shot_bodies)):
        if shot is None and body:
            shots[i] = (body[0][0], body[-1][1], shot_offsets[i])

    valid_dissolves = set()
    for index, (left, right, where) in dissolves.items():
        before = shots[index]
        after = shots[index+1] if index+1 < len(shots) else None
        target = dissolve_targets.get(index)
        expected_target = tuple(shot_labels[index:index+2])
        if target != 'adjacent' and (target is None or target != expected_target):
            add('DISSOLVE_TARGET', '叠化须指明当前镜→相邻下一镜，不得引用缺失或非相邻镜号', where)
            continue
        if not shot_bodies[index] or where <= shot_bodies[index][-1][2]:
            add('DISSOLVE_POSITION', '叠化声明必须位于前镜末段，不能提前放在其他S段', where)
            continue
        if (not all(math.isfinite(x) for x in (left, right)) or left < 0 or right <= left
                or before is None or after is None
                or abs(after[0]-left)>1e-6 or abs(before[1]-right)>1e-6
                or left <= before[0] or right >= after[1]):
            add('DISSOLVE_MISMATCH', '叠化必须对应相邻两个镜头真实重叠区间，并保留两侧非重叠画面', where)
        elif not any(abs(a-left)<1e-6 and abs(b-right)<1e-6 for a,b,_ in spans):
            add('DISSOLVE_BODY_MISSING', '主时间线应独立写出一次叠化区间及两侧画面', where)
        else:
            valid_dissolves.add(index)

    def check_spans(items, shot=False):
        previous = start
        for index, item in enumerate(items):
            if item is None:
                continue
            left, right, where = item
            if not math.isfinite(left) or not math.isfinite(right) or left < 0 or right < 0:
                add('TIME_INVALID', '时间必须为有限非负数', where)
                continue
            if abs(left - previous) > 1e-6 and not (shot and index-1 in valid_dissolves):
                add('SHOT_TIME_DISCONTINUITY' if shot else 'TIME_DISCONTINUITY', f'当前起点{left}，上一终点{previous}', where)
            if right <= left:
                add('TIME_REVERSED', '时间窗口必须正向', where)
            previous = right
        if target_end is not None and abs(previous - target_end) > 1e-6:
            add('DURATION_MISMATCH', f'{"镜头" if shot else "正文"}结束{previous}秒，要求绝对终点{target_end}秒')

    if shots:
        check_spans(shots, shot=True)
    if spans:
        check_spans(spans)
        for i, (shot, body) in enumerate(zip(shots, shot_bodies)):
            if not body:
                add('SHOT_BODY_MISSING', '本镜缺少正文时间段，无法与镜头时间窗核对', shot_offsets[i])
            elif shot is not None:
                left, right, where = shot
                expected_start = dissolves[i-1][1] if i-1 in valid_dissolves else left
                if (abs(body[0][0]-expected_start)>1e-6 or abs(body[-1][1]-right)>1e-6
                        or any(a<left-1e-6 or b>right+1e-6 for a,b,_ in body)):
                    add('SHOT_BODY_MISMATCH', '镜头头部与所属正文时间窗不一致或正文越界', where)
    elif target_end is not None or shots or profile in {'fusion', 'compact'}:
        add('UNTIMED_REVIEW', '无可解析分段时间轴，需人工核对动作容量与总时长', severity='review')
    if profile == 'fusion':
        if len(set(shot_labels)) != len(shot_labels):
            add('SHOT_ID_DUPLICATE', '镜头编号重复，无法唯一核对转场目标')
        global_header = re.search(r'^\s*【全局[^】]*】', text, re.M)
        if not global_header:
            add('GLOBAL_MISSING', '融合模板缺少全局设定')
        else:
            global_body = text[global_header.end():shot_offsets[0] if shot_offsets else len(text)]
            if not any(line.strip() and not line.strip().startswith('【') for line in global_body.splitlines()):
                add('GLOBAL_EMPTY', '全局标题下没有共享设定内容', global_header.start())
        if not shots:
            add('SHOT_MISSING', '融合模板缺少镜头头部')
        if not spans:
            add('TIMELINE_MISSING', '融合模板缺少S正文时间段')
        for i, where in enumerate(shot_offsets):
            section = text[where:shot_offsets[i+1] if i+1<len(shots) else len(text)]
            if not re.search(r'^[ \t]*画面[ \t]*[：:][ \t]*\S', section, re.M):
                add('PICTURE_MISSING', '本镜缺少非空画面布局', where)
            body_blocks = [b for b in blocks if b['shot']==i]
            if not body_blocks:
                add('SHOT_BODY_MISSING', '本镜缺少正文时间段', where)
            elif not any(value for value,_ in body_blocks[-1]['fields'].get('transition', [])):
                add('TRANSITION_MISSING', '本镜末段缺少真实衔接或结尾transition', body_blocks[-1]['span'][2])
        for block in blocks:
            if block['shot'] < 0:
                add('ORPHAN_BODY', 'S正文必须归属一个镜头', block['span'][2])
            action_lines = []
            for line_index, line in enumerate(block['lines']):
                if FIELD.match(line):
                    break
                if line_index == 0:
                    time_match = TIME.match(line)
                    line = line[time_match.end():].strip(' ：:】\n') if time_match else line
                action_lines.append(line.strip())
            if not any(action_lines):
                add('ACTION_EMPTY', '本S段缺少动作或画面状态描述', block['span'][2])
            for key in ('fx-env', 'sound'):
                values = block['fields'].get(key, [])
                if not values or not any(value for value,_ in values):
                    add('FIELD_MISSING', f'本S段缺少非空{key}', block['span'][2])
                elif len(values)>1:
                    add('FIELD_DUPLICATE', f'本S段重复{key}；合并同段内容', values[1][1])
    if contract is not None:
        check_contract(text, blocks, contract, add)
    if event_times == 'absolute':
        check_event_times(text, blocks, add)
    elif re.search(r'(?<![A-Za-z0-9_])t\s*[=≈]', mask_quotes(text), re.I):
        add('EVENT_TIME_REVIEW', 't=事件节点及相对/绝对时间需人工核对；本脚本只自动核对区间', severity='review')
    # These are review candidates, not universal bans. Preserve motivated pauses,
    # negations, screen directions, dialogue, and intentionally supernatural motion.
    for match in re.finditer(r'瞬间到达|瞬移|重新摆架|一动不动|反手|全程固定|全程高速', text):
        add('CONTEXT_REVIEW', '结合主体、因果、否定范围和时段复核: ' + match.group(), match.start(), 'review')
    return issues


def validate_contract(contract):
    if contract is None:
        return
    if not isinstance(contract, dict) or set(contract)-{'dialogue', 'sound_mode'}:
        raise ValueError('contract仅支持dialogue与sound_mode')
    if 'sound_mode' in contract and contract['sound_mode'] not in {'silent', 'unspecified'}:
        raise ValueError('sound_mode仅支持silent/unspecified；其他声音要求人工复核')
    if 'dialogue' in contract:
        if not isinstance(contract['dialogue'], list):
            raise ValueError('dialogue必须为按发声顺序排列的数组')
        for item in contract['dialogue']:
            if (not isinstance(item, dict) or set(item)!={'speaker','text'}
                    or not all(isinstance(item[k],str) and item[k].strip() for k in ('speaker','text'))):
                raise ValueError('每条对白必须只有非空speaker和text')
    if contract.get('sound_mode')=='silent' and contract.get('dialogue'):
        raise ValueError('完全静音与非空锁定对白互斥')


def check_contract(text, blocks, contract, add):
    """Only explicit sound fields and a documented quote grammar are verified."""
    sound_lines = [(match[1],match.start()) for match in
                   re.finditer(r'^[ \t]*sound[ \t]*[：:][ \t]*(.*)',text,re.M|re.I)]
    if contract.get('sound_mode') == 'silent':
        if not sound_lines:
            add('SILENCE_UNVERIFIED', '没有sound字段，无法验证完全静音', severity='review')
        for value, where in sound_lines:
            # Accept only explicit silence. Additional instructions need semantic review.
            if re.search(r'(?:对白|画内|画外|说|旁白)[^“"]*[“"][^”"]+[”"]', value):
                add('SILENCE_CONFLICT', '完全静音契约下出现明确发声对白', where)
            elif value.strip(' 。.；;') not in {'完全静音','静音','无声'}:
                add('SILENCE_REVIEW', '静音契约下出现额外sound内容；核对是否包含实际声音', where, 'review')
    if 'dialogue' not in contract:
        return
    expected = contract['dialogue']
    speakers = {item['speaker'] for item in expected}
    actual = []
    for value, where in sound_lines:
        quoted = list(re.finditer(r'“([^”]*)”|"([^"\n]*)"',value))
        previous_end = 0
        for quote in quoted:
            prefix = value[previous_end:quote.start()].strip()
            speaker = next((s for s in sorted(speakers,key=len,reverse=True)
                            if re.match(re.escape(s)+r'(?=\s|[，,:：、（(]|$)', prefix)), None)
            words = quote[1] if quote[1] is not None else quote[2]
            if speaker is None:
                add('DIALOGUE_SPEAKER', '引号内发声缺少可核验说话人；使用sound：角色，声源：“原词”', where)
            actual.append((speaker,words))
            previous_end = quote.end()
        if any(mark in value for mark in ('“','”','"')):
            consumed = ''.join(q.group() for q in quoted)
            if any(value.count(mark)!=consumed.count(mark) for mark in ('“','”','"')):
                add('DIALOGUE_SYNTAX', '对白引号未配对或含不支持的嵌套引号', where)
        if re.search(r'(?:对白|说|画内|画外|旁白)\s*[：:]', value[previous_end:]):
            add('DIALOGUE_UNPARSED', '疑似无引号对白，无法逐字核验', where)
    def merged(items):
        output=[]
        for speaker,words in items:
            if output and output[-1][0]==speaker:
                output[-1]=(speaker,output[-1][1]+words)
            else:
                output.append((speaker,words))
        return output
    if merged(actual)!=merged((x['speaker'],x['text']) for x in expected):
        add('DIALOGUE_MISMATCH', 'sound中的说话人、发声顺序或逐字台词与原文不一致')


def point(value):
    if not isinstance(value, list) or len(value) != 2 or any(
        not finite_number(n) for n in value
    ):
        raise ValueError('坐标必须为两个有限数字组成的数组')
    return value


def intersects(a, b, low, high):
    """Closed segment vs closed axis-aligned box, including tangent contact."""
    lo, hi = 0.0, 1.0
    for i in range(2):
        delta = b[i] - a[i]
        if abs(delta) < 1e-12:
            if not low[i] <= a[i] <= high[i]:
                return False
        else:
            t1, t2 = (low[i] - a[i]) / delta, (high[i] - a[i]) / delta
            lo, hi = max(lo, min(t1, t2)), min(hi, max(t1, t2))
            if lo > hi:
                return False
    return True


def check_geometry(data):
    if not isinstance(data, dict):
        raise ValueError('几何文件根节点必须为对象')
    geometry_keys = {'projections', 'routes', 'axes', 'distances', 'motions', 'dynamic_axes'}
    if set(data) - geometry_keys:
        raise ValueError('几何根节点仅支持' + '/'.join(sorted(geometry_keys)) + '，检查字段拼写')
    def objects(value, label):
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise ValueError(label + '必须为对象数组')
        return value
    for key in geometry_keys:
        objects(data.get(key, []), key)
    issues = []
    def add(code, index, message):
        issues.append(dict(code=code, severity='error', item=index, message=message))
    def scalar(value, label):
        if not finite_number(value):
            raise ValueError(label + '必须为有限数字')
        return value
    def fields(item, allowed, required, label):
        if set(item) - allowed or required - set(item):
            raise ValueError(label + '字段缺失或存在未知字段')
    def distance(a, b):
        return math.hypot(a[0]-b[0], a[1]-b[1])
    for index, item in enumerate(data.get('projections', [])):
        fields(item, {'camera','look_at','subject','facing','screen','view'},
               {'camera','look_at','subject'}, 'projections')
        if 'view' in item and 'facing' not in item:
            raise ValueError('检验view必须提供facing朝向')
        c, t, p = (point(item[k]) for k in ('camera', 'look_at', 'subject'))
        d, v = [t[i] - c[i] for i in range(2)], [p[i] - c[i] for i in range(2)]
        norm = math.hypot(*d)
        if norm < 1e-9:
            raise ValueError('机位和看向目标不能重合')
        depth = sum(d[i] * v[i] for i in range(2)) / norm
        horizontal = (v[0] * d[1] - v[1] * d[0]) / norm
        actual = 'right' if horizontal > 1e-6 else 'left' if horizontal < -1e-6 else 'center'
        if depth <= 0:
            add('BEHIND_CAMERA', index, '主体不在摄影机前向半平面')
        if 'screen' in item:
            if item['screen'] not in {'left', 'right', 'center'}:
                raise ValueError('screen仅支持left/right/center')
            if item['screen'] != actual:
                add('SCREEN_PROJECTION', index, f'声称{item["screen"]}，平面计算为{actual}')
        if 'facing' in item:
            f = point(item['facing'])
            denom = math.hypot(*f) * math.hypot(*v)
            if denom < 1e-9:
                raise ValueError('人物朝向非零，人物不能与摄影机重合')
            cosine = -sum(f[i] * v[i] for i in range(2)) / denom
            view = item.get('view')
            if view not in {None, 'front', 'back', 'side'}:
                raise ValueError('view仅支持front/back/side')
            if (view == 'front' and cosine <= 0) or (view == 'back' and cosine >= 0) or (view == 'side' and abs(cosine) > .5):
                add('FACING_MISMATCH', index, '声称的可见面与身体朝向/机位不符')
    for index, item in enumerate(data.get('routes', [])):
        fields(item, {'points','obstacles'}, {'points'}, 'routes')
        if not isinstance(item['points'], list):
            raise ValueError('points必须为坐标数组')
        pts = [point(p) for p in item['points']]
        if len(pts) < 2:
            raise ValueError('路线至少含起终两个节点')
        for obstacle in objects(item.get('obstacles', []), 'obstacles'):
            fields(obstacle, {'min','max'}, {'min','max'}, 'obstacles')
            low, high = point(obstacle['min']), point(obstacle['max'])
            if any(low[i] > high[i] for i in range(2)):
                raise ValueError('障碍min不得大于max')
            if any(intersects(a, b, low, high) for a, b in zip(pts, pts[1:])):
                add('ROUTE_OBSTACLE', index, '路线线段与障碍相交；需绕行或明确合法跨越')
    for index, item in enumerate(data.get('axes', [])):
        fields(item, {'a','b','cameras','bridge'}, {'a','b','cameras'}, 'axes')
        a, b = point(item['a']), point(item['b'])
        if a == b:
            raise ValueError('轴线两个端点不能重合')
        if not isinstance(item['cameras'], list):
            raise ValueError('cameras必须为坐标数组')
        cameras = [point(c) for c in item['cameras']]
        if len(cameras) < 2:
            raise ValueError('轴线检查至少两个机位')
        signs = [(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]) for c in cameras]
        bridge = item.get('bridge')
        if bridge not in {None, 'visible_crossing', 'neutral_shot', 'reestablish'}:
            raise ValueError('过轴桥接类型无效')
        nonzero = [s for s in signs if abs(s) > 1e-9]
        if any(x*y < 0 for x, y in zip(nonzero, nonzero[1:])) and bridge is None:
            add('AXIS_CROSSING', index, '机位换侧，未记录可见过轴/中性镜头/空间重建证据')
    for index, item in enumerate(data.get('distances', [])):
        fields(item, {'a','b','min','max','claimed','tolerance'}, {'a','b'}, 'distances')
        if not {'min','max','claimed'} & set(item):
            raise ValueError('distances至少给min/max/claimed之一')
        actual = distance(point(item['a']), point(item['b']))
        tolerance = scalar(item.get('tolerance', 1e-6), 'tolerance')
        if tolerance < 0:
            raise ValueError('tolerance不得为负')
        bounds = {key: scalar(item[key], key) for key in ('min','max','claimed') if key in item}
        if any(value < 0 for value in bounds.values()):
            raise ValueError('距离不得为负')
        if 'min' in bounds and 'max' in bounds and bounds['min'] > bounds['max']:
            raise ValueError('距离min不得大于max')
        if (('min' in bounds and actual < bounds['min']-tolerance)
                or ('max' in bounds and actual > bounds['max']+tolerance)
                or ('claimed' in bounds and abs(actual-bounds['claimed']) > tolerance)):
            add('DISTANCE_MISMATCH', index, f'声明距离与显式平面位置不符；实际{actual:.6g}')
    for index, item in enumerate(data.get('motions', [])):
        fields(item, {'from','to','facing','direction','target_from','target_to',
                      'distance_change','duration','max_speed'}, {'from','to'}, 'motions')
        start, end = point(item['from']), point(item['to'])
        movement = [end[i]-start[i] for i in range(2)]
        length = math.hypot(*movement)
        direction = item.get('direction')
        if direction not in {None, 'forward', 'backward', 'lateral'}:
            raise ValueError('direction仅支持forward/backward/lateral')
        if 'facing' in item:
            facing = point(item['facing'])
            if math.hypot(*facing) < 1e-9:
                raise ValueError('facing必须为非零朝向向量')
        if direction is not None:
            if 'facing' not in item:
                raise ValueError('direction检查需要facing')
            cosine = sum(facing[i]*movement[i] for i in range(2)) / (math.hypot(*facing)*length) if length > 1e-9 else None
            if (cosine is None or (direction == 'forward' and cosine <= 1e-6)
                    or (direction == 'backward' and cosine >= -1e-6)
                    or (direction == 'lateral' and abs(cosine) > 1e-6)):
                add('MOTION_DIRECTION', index, '声明移动方向与当前固定朝向/直段位移不符')
        change = item.get('distance_change')
        if change not in {None, 'closer', 'farther', 'unchanged'}:
            raise ValueError('distance_change仅支持closer/farther/unchanged')
        if 'target_to' in item and 'target_from' not in item:
            raise ValueError('target_to需要target_from')
        if 'target_from' in item:
            target_start = point(item['target_from'])
            target_end = point(item.get('target_to', item['target_from']))
        if change is not None:
            if 'target_from' not in item:
                raise ValueError('distance_change检查需要target_from')
            delta = distance(end, target_end)-distance(start, target_start)
            if ((change == 'closer' and delta >= -1e-6)
                    or (change == 'farther' and delta <= 1e-6)
                    or (change == 'unchanged' and abs(delta) > 1e-6)):
                add('DISTANCE_CHANGE', index, f'声明距变与双方位置不符；距离变化{delta:.6g}')
        if 'duration' in item:
            duration = scalar(item['duration'], 'duration')
            if duration <= 0:
                raise ValueError('duration必须为正')
        if 'max_speed' in item:
            if 'duration' not in item:
                raise ValueError('max_speed检查需要duration')
            cap = scalar(item['max_speed'], 'max_speed')
            if cap < 0:
                raise ValueError('max_speed不得为负')
            if length > cap*duration+1e-6:
                add('MOTION_BUDGET', index, '最短平面行程已超过显式速度/用时预算；不代表完整路径模拟')
    for index, item in enumerate(data.get('dynamic_axes', [])):
        fields(item, {'frames','bridge'}, {'frames'}, 'dynamic_axes')
        frames = objects(item['frames'], 'frames')
        if len(frames) < 2:
            raise ValueError('dynamic_axes至少两个采样状态')
        signs = []
        for frame in frames:
            fields(frame, {'a','b','camera'}, {'a','b','camera'}, 'dynamic_axes.frames')
            a, b, c = (point(frame[key]) for key in ('a','b','camera'))
            if distance(a, b) < 1e-9:
                raise ValueError('动态轴端点重合；需选有效行动轴或重新建立')
            signs.append((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
        bridge = item.get('bridge')
        if bridge not in {None, 'visible_crossing', 'neutral_shot', 'reestablish'}:
            raise ValueError('动态过轴桥接类型无效')
        nonzero = [value for value in signs if abs(value) > 1e-9]
        if any(x*y < 0 for x,y in zip(nonzero, nonzero[1:])) and bridge is None:
            add('DYNAMIC_AXIS_CROSSING', index, '人物/机位变化导致动态轴采样侧符号反转，未记录桥接证据')
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prompt', type=Path)
    parser.add_argument('--duration', type=float)
    parser.add_argument('--start', type=float, default=0, help='全片绝对起点；默认0')
    parser.add_argument('--end', type=float, help='全片绝对终点；duration为其旧别名')
    parser.add_argument('--profile', choices=['basic','fusion','compact','prose'], default='basic')
    parser.add_argument('--contract', type=Path, help='原对白与可选静音契约JSON')
    parser.add_argument('--reference', action='append', default=[])
    parser.add_argument('--allow-platform-params', action='store_true')
    parser.add_argument('--geometry', type=Path)
    parser.add_argument('--event-times', choices=['review', 'absolute'], default='review',
                        help='默认人工复核；absolute仅验显式S段内绝对t=数值范围及行动段顺序')
    args = parser.parse_args()
    try:
        if args.duration is not None and (not math.isfinite(args.duration) or args.duration <= 0):
            raise ValueError('duration必须为有限正数')
        prompt_text = args.prompt.read_text(encoding='utf-8-sig')
        contract = load_input_json(args.contract) if args.contract else None
        findings = check_text(prompt_text, args.duration, args.reference, args.allow_platform_params,
                              start=args.start, end=args.end, profile=args.profile, contract=contract,
                              event_times=args.event_times)
        has_timeline = any(TIME.match(line) for line in prompt_text.splitlines())
        if not has_timeline and args.profile != 'prose' and not any(f['code']=='UNTIMED_REVIEW' for f in findings):
            findings.append(dict(code='UNTIMED_REVIEW',severity='review',line=1,
                                 message='没有可解析正文时间轴；若用户指定自然叙述，使用prose模式'))
        if args.geometry:
            findings += check_geometry(load_input_json(args.geometry))
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, OverflowError) as exc:
        print(json.dumps({'status':'INPUT_ERROR', 'message':str(exc)}, ensure_ascii=False))
        return 2
    failed = any(i['severity'] == 'error' for i in findings)
    review = any(i['severity'] == 'review' for i in findings)
    print(json.dumps({'status':'CHECK_FAILED' if failed else 'TEXT_REVIEW_REQUIRED' if review else 'TEXT_CHECK_PASS',
                      'semantic_review':'REQUIRED', 'video_validation':'NOT_RUN',
                      'profile':args.profile,
                      'timeline_validation':'RUN' if has_timeline else 'NOT_RUN',
                      'template_validation':'RUN' if args.profile=='fusion' else 'NOT_RUN',
                      'dialogue_validation':'EXPLICIT_QUOTES_ONLY' if contract is not None and 'dialogue' in contract else 'NOT_RUN',
                      'sound_validation':'EXPLICIT_SILENCE_ONLY' if contract and contract.get('sound_mode')=='silent' else 'NOT_RUN',
                      'event_time_validation':('ABSOLUTE_NUMERIC_ONLY' if args.event_times=='absolute'
                                               and EVENT.search(mask_quotes(prompt_text)) else 'NOT_RUN'),
                      'geometry_scope':'explicit_2d_data_only' if args.geometry else 'NOT_RUN',
                      'findings':findings}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
