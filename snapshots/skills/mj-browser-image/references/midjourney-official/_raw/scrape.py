# -*- coding: utf-8 -*-
"""抓取 Midjourney 官方文档文章，转 Markdown 并把图片本地化。v2"""
import os, re, sys, time, json, mimetypes
from urllib.parse import urljoin, unquote
from curl_cffi import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = "https://docs.midjourney.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(DOCS, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

SESSION = requests.Session(impersonate="chrome")
IMG_MAP = {}

def get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            r = SESSION.get(url, timeout=45)
            if r.status_code == 200 and "Just a moment" not in r.text:
                return r
            last = f"status={r.status_code}"
        except Exception as e:
            last = repr(e)
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"fetch failed {url}: {last}")

def slugify(t):
    t = re.sub(r"[^\w\s-]", "", t, flags=re.UNICODE).strip()
    return re.sub(r"[\s_]+", "-", t)[:80] or "untitled"

def download_img(src, slug, ctx):
    url = urljoin(BASE, src)
    key = (slug, url)
    if key in IMG_MAP:
        return IMG_MAP[key]
    try:
        r = SESSION.get(url, timeout=60)
        if r.status_code != 200:
            return None
        ctype = r.headers.get("content-type", "").split(";")[0].strip()
        ext = mimetypes.guess_extension(ctype) if ctype else None
        if not ext:
            m = re.search(r"\.(png|jpe?g|gif|webp|svg|mp4|webm)$", unquote(url), re.I)
            ext = "." + m.group(1).lower() if m else ".png"
        if ext == ".jpe":
            ext = ".jpg"
        ctx["n"] += 1
        name = f"img{ctx['n']:02d}{ext}"
        d = os.path.join(ASSETS, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, name), "wb") as f:
            f.write(r.content)
        rel = f"assets/{slug}/{name}"
        IMG_MAP[key] = rel
        return rel
    except Exception:
        return None

def inline(node, slug, ctx):
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(str(c))
        elif isinstance(c, Tag):
            n = c.name
            if n in ("script", "style", "noscript"):
                continue
            if n == "br":
                out.append("  \n")
            elif n in ("strong", "b"):
                out.append(f"**{inline(c, slug, ctx)}**")
            elif n in ("em", "i"):
                out.append(f"*{inline(c, slug, ctx)}*")
            elif n == "code":
                out.append(f"`{c.get_text()}`")
            elif n == "a":
                txt = inline(c, slug, ctx).strip()
                href = c.get("href", "")
                href = urljoin(BASE, href) if href else ""
                if txt and href and "#" not in href.split("/")[-1]:
                    out.append(f"[{txt}]({href})")
                else:
                    out.append(txt)
            elif n == "img":
                alt = c.get("alt", "") or ""
                rel = download_img(c.get("src", ""), slug, ctx)
                if rel:
                    out.append(f"![{alt}]({rel})")
            else:
                out.append(inline(c, slug, ctx))
    return "".join(out)

def clean(t):
    t = t.replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return t.strip()

def table_md(tb, slug, ctx):
    rows = []
    for tr in tb.find_all("tr"):
        cells = [clean(inline(td, slug, ctx)) for td in tr.find_all(["th", "td"])]
        if cells and any(cells):
            rows.append(cells)
    if not rows:
        return ""
    w = max(len(r) for r in rows)
    rows = [r + [""] * (w - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |",
           "|" + "|".join([" --- "] * w) + "|"]
    for r in rows[1:]:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)

def convert(container, slug):
    lines = []
    ctx = {"n": 0}
    media = []

    def emit(block):
        if block and block.strip():
            lines.append(block.strip())

    def walk(node):
        for c in node.children:
            if not isinstance(c, Tag):
                continue
            n = c.name
            if n in ("script", "style", "noscript", "nav"):
                continue
            if n in ("h1", "h2", "h3", "h4", "h5", "h6"):
                lv = min(int(n[1]), 6)
                t = clean(inline(c, slug, ctx))
                if t:
                    emit(f"{'#' * lv} {t}")
            elif n == "p":
                txt = clean(inline(c, slug, ctx))
                cls = " ".join(c.get("class") or [])
                if txt:
                    if "custom_warning" in cls or "custom_compatible" in cls or "custom_note" in cls:
                        emit("> " + txt.replace("\n", "\n> "))
                    else:
                        emit(txt)
            elif n == "ul":
                for li in c.find_all("li", recursive=False):
                    label = (li.get("title") or "").strip()
                    if label:
                        emit(f"**{label}**")
                    for ch in li.children:
                        if not isinstance(ch, Tag):
                            continue
                        if ch.name == "p":
                            t = clean(inline(ch, slug, ctx))
                            if t:
                                emit(t)
                        elif ch.name in ("ul", "ol"):
                            for sub in ch.find_all("li", recursive=False):
                                t = clean(inline(sub, slug, ctx))
                                if t:
                                    emit(f"- {t}")
                        elif ch.name == "img":
                            rel = download_img(ch.get("src", ""), slug, ctx)
                            if rel:
                                emit(f"![{ch.get('alt','') or 'image'}]({rel})")
            elif n == "ol":
                for i, li in enumerate(c.find_all("li", recursive=False), 1):
                    t = clean(inline(li, slug, ctx))
                    if t:
                        emit(f"{i}. {t}")
            elif n == "table":
                t = table_md(c, slug, ctx)
                if t:
                    emit(t)
            elif n == "pre":
                emit("```\n" + c.get_text().rstrip() + "\n```")
            elif n == "blockquote":
                t = clean(inline(c, slug, ctx))
                if t:
                    emit("> " + t.replace("\n", "\n> "))
            elif n == "figure":
                img = c.find("img")
                cap = clean(inline(c.find("figcaption"), slug, ctx)) if c.find("figcaption") else ""
                if img:
                    rel = download_img(img.get("src", ""), slug, ctx)
                    if rel:
                        emit(f"![{cap or 'image'}]({rel})")
                        if cap:
                            emit(f"*{cap}*")
            elif n == "img":
                rel = download_img(c.get("src", ""), slug, ctx)
                if rel:
                    emit(f"![{c.get('alt','') or 'image'}]({rel})")
            elif n == "iframe":
                src = urljoin(BASE, c.get("src", "") or "")
                media.append(("iframe", src))
                emit(f"> 嵌入媒体：{src}")
            elif n == "video":
                src = c.get("src", "")
                if not src:
                    s = c.find("source")
                    src = s.get("src", "") if s else ""
                src = urljoin(BASE, src) if src else ""
                media.append(("video", src))
                emit(f"> 视频：{src}")
            elif n in ("div", "section", "article", "details", "summary"):
                walk(c)
            else:
                t = clean(inline(c, slug, ctx))
                if t:
                    emit(t)

    walk(container)
    txt = "\n\n".join(lines)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip(), media

def fetch_article(aid):
    url = f"{BASE}/hc/en-us/articles/{aid}"
    r = get(url)
    s = BeautifulSoup(r.text, "html.parser")
    h1 = s.find("h1")
    title = clean(h1.get_text()) if h1 else aid
    body = s.select_one("section.article-content") or s.select_one("article")
    if body is None:
        raise RuntimeError("no body")
    md, media = convert(body, slugify(title))
    return title, md, media

ARTICLES = [
    ("27870484040333", "Comparing Plans"),
    ("31974654274573", "How to Subscribe"),
    ("33390994570509", "Logging In"),
    ("32023408776205", "Prompt Basics"),
    ("32835253061645", "Art of Prompting"),
    ("39193335040013", "Moodboards"),
    ("32433330574221", "Personalization"),
    ("33329329805581", "Modifying Creations"),
    ("37460773864589", "Video"),
    ("31894244298125", "Aspect Ratio"),
    ("32634113811853", "Raw"),
    ("32199405667853", "Version"),
    ("35577175650957", "Draft Mode"),
    ("32196176868109", "Stylize"),
    ("32390120435085", "Weird"),
    ("32099348346765", "Variety"),
    ("32016412137741", "GPU Speed"),
    ("32019750070669", "Stealth"),
    ("32040250122381", "Image Prompts"),
    ("32180011136653", "Style References"),
    ("48495453462797", "Edit Model"),
    ("33390732264589", "Creating on Web"),
    ("33329462451469", "Organizing Creations"),
    ("32013696484109", "Community Guidelines"),
    ("32638309968141", "Billing Contact"),
]

if __name__ == "__main__":
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    report = []
    for i, (aid, label) in enumerate(ARTICLES, 1):
        if only and aid not in only:
            continue
        try:
            title, md, media = fetch_article(aid)
            fn = f"{i:02d}_{slugify(title)}.md"
            head = (f"# {title}\n\n> 来源：{BASE}/hc/en-us/articles/{aid}\n"
                    f"> 抓取时间：2026-11-05\n\n---\n\n")
            with open(os.path.join(DOCS, fn), "w", encoding="utf-8") as f:
                f.write(head + md + "\n")
            report.append({"i": i, "id": aid, "title": title, "file": fn,
                           "chars": len(md), "media": media})
            print(f"[{i:02d}] OK  {title}  {len(md)} chars  media={len(media)}")
        except Exception as e:
            print(f"[{i:02d}] FAIL {label} ({aid})  {e}")
            report.append({"i": i, "id": aid, "title": label, "error": str(e)})
        time.sleep(0.6)
    os.makedirs(os.path.join(ROOT, "_raw"), exist_ok=True)
    with open(os.path.join(ROOT, "_raw", "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print("done", len(report))
