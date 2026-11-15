#!/usr/bin/env python3
"""greatwall生图新：独立的文生图与图片编辑客户端。"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from PIL import Image


BASE_URL = "https://api.gwlink.cc/v1"
API_KEY_ENV = "GATEWAY_IMAGE_NEW_API_KEY"
SUPPORTED_MODELS = (
    "gpt-image-2-高质量4k",
    "gpt-image-2.5-exact",
    "gpt-image-2.5-flare",
    "gpt-image-2.5-sunburst",
)


def get_env(name: str) -> str | None:
    value = os.environ.get(name)
    if value:
        return value
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except OSError:
        return None


def image_file(path: Path) -> tuple[str, bytes, str]:
    payload = path.read_bytes()
    with Image.open(io.BytesIO(payload)) as image:
        if image.format not in ("PNG", "JPEG", "WEBP"):
            raise ValueError(f"输入图片必须是 PNG、JPEG 或 WebP：{path}")
        mime = Image.MIME[image.format]
        image.verify()
    return path.name, payload, mime


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="greatwall生图新：生成前必须由用户选择模型")
    parser.add_argument("mode", choices=("generate", "edit"))
    parser.add_argument("--model", required=True, choices=SUPPORTED_MODELS)
    prompts = parser.add_mutually_exclusive_group(required=True)
    prompts.add_argument("--prompt")
    prompts.add_argument("--prompt-file", type=Path, help="UTF-8 提示词文件")
    parser.add_argument("--out", type=Path, required=True, help="新建 PNG 文件，禁止覆盖")
    parser.add_argument("--image", type=Path, action="append", default=[], help="编辑输入，可重复指定")
    parser.add_argument("--mask", type=Path, help="可选 PNG 蒙版，是否生效取决于模型")
    parser.add_argument("--size", help="仅填写已确认被所选模型支持的尺寸")
    parser.add_argument("--quality", choices=("auto", "low", "medium", "high"), default="auto")
    parser.add_argument("--response-format", choices=("url", "b64_json"), default="url")
    parser.add_argument("--timeout", type=float, default=1000)
    args = parser.parse_args(argv)
    if args.mode == "generate" and (args.image or args.mask):
        parser.error("文生图不能传 --image 或 --mask，请使用 edit")
    if args.mode == "edit" and not args.image:
        parser.error("图生图至少需要一个 --image")
    if args.out.suffix.lower() != ".png":
        parser.error("输出文件请使用 .png 后缀")
    if args.timeout <= 0:
        parser.error("--timeout 必须大于 0")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    api_key = ""
    image_url = None
    stage = "prepare"
    try:
        prompt = args.prompt_file.read_text(encoding="utf-8-sig") if args.prompt_file else args.prompt
        if not prompt or not prompt.strip():
            raise ValueError("提示词不能为空")
        out = args.out.expanduser().resolve()
        if out.exists():
            raise FileExistsError(f"输出已存在，换一个新文件名：{out}")
        files = [("image", image_file(path)) for path in args.image]
        if args.mask:
            mask_file = image_file(args.mask)
            with Image.open(io.BytesIO(mask_file[1])) as mask, Image.open(io.BytesIO(files[0][1][1])) as first:
                if mask.format != "PNG" or mask.size != first.size:
                    raise ValueError("蒙版必须为 PNG，且尺寸与第一张输入图片一致")
            files.append(("mask", mask_file))
        out.parent.mkdir(parents=True, exist_ok=True)
        api_key = get_env(API_KEY_ENV) or ""
        if not api_key:
            raise ValueError(f"未配置专用密钥变量 {API_KEY_ENV}")
        request = {
            "model": args.model,
            "prompt": prompt,
            "n": 1,
            "quality": args.quality,
            "response_format": args.response_format,
        }
        if args.size:
            request["size"] = args.size
        with httpx.Client(timeout=args.timeout) as client:
            stage = args.mode
            # 不重发生成请求：超时或服务错误后可能已经计费。
            headers = {"Authorization": f"Bearer {api_key}"}
            if args.mode == "edit":
                response = client.post(BASE_URL + "/images/edits", headers=headers, data=request, files=files)
            else:
                response = client.post(BASE_URL + "/images/generations", headers=headers, json=request)
            response.raise_for_status()
            data = response.json().get("data")
            if not isinstance(data, list) or not data or not isinstance(data[0], dict):
                raise ValueError("接口没有返回可用的图片数据")
            item = data[0]
            stage = "decode"
            if item.get("b64_json"):
                payload = base64.b64decode(item["b64_json"], validate=True)
            elif item.get("url"):
                image_url = item["url"]
                url = urlsplit(image_url)
                if url.scheme != "https" or not url.hostname or url.username or url.password:
                    raise ValueError("接口返回的图片链接必须是无账号信息的 HTTPS 地址")
                stage = "download"
                downloaded = client.get(image_url, timeout=120, follow_redirects=True)
                downloaded.raise_for_status()
                payload = downloaded.content
            else:
                raise ValueError("接口既没有返回图片链接，也没有返回 Base64 图片")
        stage = "decode"
        with Image.open(io.BytesIO(payload)) as image:
            if image.format not in ("PNG", "JPEG", "WEBP"):
                raise ValueError("生成结果不是 PNG、JPEG 或 WebP 图片")
            image.load()
            width, height = image.size
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            payload = buffer.getvalue()
        stage = "save"
        with out.open("xb") as output:
            try:
                output.write(payload)
            except OSError:
                output.close()
                out.unlink()
                raise
        print(json.dumps({"ok": True, "mode": args.mode, "model": args.model, "path": str(out),
                          "bytes": len(payload), "width": width, "height": height}, ensure_ascii=False))
        return 0
    except Exception as exc:
        message = str(exc)
        if isinstance(exc, httpx.HTTPStatusError):
            message = f"HTTP {exc.response.status_code}"
            try:
                detail = exc.response.json().get("error", {})
                if isinstance(detail, dict) and detail.get("message"):
                    message += ": " + str(detail["message"])
            except (ValueError, AttributeError):
                pass
        if isinstance(exc, httpx.TimeoutException) and stage in ("generate", "edit"):
            message = "生成请求超时，服务器可能已收到任务。请先查看平台图片任务日志，不要自动重新生成。"
        if api_key:
            message = message.replace(api_key, "[REDACTED]")
        result = {"ok": False, "stage": stage, "error": message[:600], "generation_retried": False}
        if image_url:
            result["image_url"] = image_url.replace(api_key, "[REDACTED]") if api_key else image_url
            result["next_step"] = "先处理现有结果或重下此链接，不要再次提交生成请求。"
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
