# -*- coding: utf-8 -*-
"""抓取 billing 分类页下的全部文章。"""
import os, re, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrape import fetch_article, slugify, DOCS, ROOT, SESSION, clean
from bs4 import BeautifulSoup

CAT = "https://docs.midjourney.com/hc/en-us/categories/16016577793421"
DONE_IDS = {"31974654274573", "27870484040333", "32016412137741", "33390994570509"}

r = SESSION.get(CAT, timeout=45)
s = BeautifulSoup(r.text, "html.parser")
items, seen = [], set()
for a in s.select("a[href*='/articles/']"):
    t = a.get_text(strip=True)
    h = a["href"]
    m = re.search(r"/articles/(\d+)", h)
    if not (t and m):
        continue
    aid = m.group(1)
    if aid in seen or aid in DONE_IDS:
        continue
    seen.add(aid)
    items.append((aid, t))

print("待抓取:", len(items))
report = []
for i, (aid, label) in enumerate(items, 26):
    try:
        title, md, media = fetch_article(aid)
        fn = f"{i:02d}_{slugify(title)}.md"
        head = (f"# {title}\n\n> 来源：https://docs.midjourney.com/hc/en-us/articles/{aid}\n"
                f"> 抓取时间：2026-11-05\n\n---\n\n")
        with open(os.path.join(DOCS, fn), "w", encoding="utf-8") as f:
            f.write(head + md + "\n")
        report.append({"i": i, "id": aid, "title": title, "file": fn,
                       "chars": len(md), "media": media})
        print(f"[{i:02d}] OK  {title}  {len(md)} chars")
    except Exception as e:
        print(f"[{i:02d}] FAIL {label} ({aid})  {e}")
        report.append({"i": i, "id": aid, "title": label, "error": str(e)})
    time.sleep(0.6)

p = os.path.join(ROOT, "_raw", "report_billing.json")
with open(p, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print("done", len(report))
