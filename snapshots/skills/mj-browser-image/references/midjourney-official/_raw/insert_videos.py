# -*- coding: utf-8 -*-
"""把已下载的 YouTube 教程视频插入对应 md 段落之后。"""
import os, re, glob, subprocess, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = os.path.join(ROOT, "assets", "videos")

def dur(p):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", p],
            capture_output=True, text=True, timeout=30).stdout.strip()
        s = float(out)
        return f"{int(s // 60)}:{int(s % 60):02d}"
    except Exception:
        return ""

available = {}
for f in glob.glob(os.path.join(VID, "v_*.mp4")):
    vid = os.path.basename(f)[2:-4]
    available[vid] = f

print("可用视频:", len(available), sorted(available))

inserted = 0
for md in sorted(glob.glob(os.path.join(ROOT, "docs", "*.md"))):
    txt = open(md, encoding="utf-8").read()
    if "<video controls src=\"assets/videos/" in txt:
        continue
    lines = txt.split("\n")
    out = []
    changed = False
    for ln in lines:
        out.append(ln)
        m = re.search(r"https://youtu\.be/([A-Za-z0-9_-]+)", ln)
        if m and m.group(1) in available:
            vid = m.group(1)
            d = dur(available[vid])
            out.append("")
            out.append(f'<video controls preload="metadata" src="assets/videos/v_{vid}.mp4" width="100%"></video>')
            out.append("")
            out.append(f"*视频教程 · {d} · 本地文件 `assets/videos/v_{vid}.mp4`*")
            changed = True
            inserted += 1
    if changed:
        open(md, "w", encoding="utf-8").write("\n".join(out))

print("插入视频块:", inserted)
