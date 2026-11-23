#!/usr/bin/env python3
"""簡報的程式檢查（loop／graph 共用）。

用法：python3 scripts/check_slides.py <deck.html> [--wiki wiki] [--report reports/slides_check.md] [--no-render]

簡報格式約定（見 .agents/skills/slides-loop/SKILL.md）：
- 每張投影片是 <section class="slide">；封面加 data-type="title"（不檢查出處與結構）。
- 每張內容投影片要有 class="core"（核心重點）與 class="summary"（小結）。
- 每個重點（.core、li、.summary）都要有 [wiki:slug] 標記，slug 必須是 wiki/ 中存在的頁面。

檢查項目：
- S1 張數 8–15
- S2 每個重點都有 [wiki:slug]
- S3 [wiki:slug] 指向存在的頁面
- S4 投影片中的數字（百分比、年份、x=數字等）在所引用的 wiki 頁面中找得到
- S5 每張內容投影片有「核心重點」與「小結」
- S6 渲染檢查：1280×720 下每張投影片沒有內容溢出（需要 playwright）
有錯誤時 exit code = 1。
"""
import argparse
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Asia/Taipei")
except Exception:  # pragma: no cover
    TZ = None

CITE_RE = re.compile(r"\[wiki:([\w/\-]+)\]")
NUM_RE = re.compile(r"\d+(?:\.\d+)?\s*%|(?<![\d.])(?:19|20)\d{2}(?![\d%])|\b\d+/\d+\b|[xX]\s*=\s*\d+|\d+(?:\.\d+)?\s*k\b")


class DeckParser(HTMLParser):
    """收集每張 slide 的文字、各重點元素的文字。"""

    POINT_TAGS = {"li"}

    def __init__(self):
        super().__init__()
        self.slides = []
        self.stack = []  # (tag, classes, buffer-or-None)
        self.cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if tag == "section" and "slide" in classes:
            self.cur = {"type": a.get("data-type", ""), "text": "", "points": [], "core": None, "summary": None}
            self.slides.append(self.cur)
        buf = None
        if self.cur is not None and (tag in self.POINT_TAGS or "core" in classes or "summary" in classes):
            kind = "core" if "core" in classes else "summary" if "summary" in classes else "point"
            buf = {"kind": kind, "text": ""}
        self.stack.append((tag, buf))

    def handle_endtag(self, tag):
        while self.stack:
            t, buf = self.stack.pop()
            if buf is not None and self.cur is not None:
                txt = re.sub(r"\s+", " ", buf["text"]).strip()
                if buf["kind"] == "core":
                    self.cur["core"] = txt
                elif buf["kind"] == "summary":
                    self.cur["summary"] = txt
                self.cur["points"].append((buf["kind"], txt))
            if t == "section" and self.cur is not None and t == tag:
                self.cur = None
            if t == tag:
                break

    def handle_data(self, data):
        if self.cur is not None:
            self.cur["text"] += data
            for _, buf in self.stack:
                if buf is not None:
                    buf["text"] += data


def wiki_pages(wiki: Path):
    pages = {}
    for p in wiki.rglob("*.md"):
        slug = p.relative_to(wiki).with_suffix("").as_posix()
        pages[slug] = p.read_text(encoding="utf-8")
    return pages


def norm_num(s: str) -> str:
    return re.sub(r"\s+", "", s).lower()


def render_check(deck: Path):
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None, ["S6 無法執行渲染檢查：沒有安裝 playwright"]
    problems = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto(deck.resolve().as_uri())
        n = pg.evaluate("document.querySelectorAll('section.slide').length")
        for i in range(n):
            res = pg.evaluate(
                """(i) => {
                const ss = [...document.querySelectorAll('section.slide')];
                ss.forEach((s, j) => { s.style.display = (j === i) ? '' : 'none'; s.classList.toggle('active', j === i); });
                const s = ss[i];
                const r = s.getBoundingClientRect();
                let over = s.scrollHeight > s.clientHeight + 2 || s.scrollWidth > s.clientWidth + 2;
                let bad = [];
                s.querySelectorAll('*').forEach(e => {
                  const q = e.getBoundingClientRect();
                  if (q.width && (q.bottom > Math.min(r.bottom, window.innerHeight) + 2 || q.right > Math.min(r.right, window.innerWidth) + 2)) {
                    bad.push((e.innerText || e.tagName).slice(0, 30));
                  }
                });
                return {over, bad: bad.slice(0, 3), h: r.height};
            }""",
                i,
            )
            if res["over"] or res["bad"]:
                problems.append(f"S6 第 {i+1} 張內容溢出 1280×720 畫面：{'；'.join(res['bad']) or '捲動高度超出'}")
        b.close()
    return n, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--wiki", default="wiki")
    ap.add_argument("--report", default="reports/slides_check.md")
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()

    deck = Path(args.deck)
    pages = wiki_pages(Path(args.wiki))
    parser = DeckParser()
    parser.feed(deck.read_text(encoding="utf-8"))
    slides = parser.slides
    errors = []

    if not (8 <= len(slides) <= 15):
        errors.append(f"S1 張數為 {len(slides)}，應為 8–15 張（找不到 section.slide 時為 0）")

    for i, s in enumerate(slides, 1):
        if s["type"] == "title":
            continue
        if not s["core"]:
            errors.append(f"S5 第 {i} 張缺少「核心重點」（.core）")
        if not s["summary"]:
            errors.append(f"S5 第 {i} 張缺少「小結」（.summary）")
        cited = set()
        for kind, txt in s["points"]:
            cs = CITE_RE.findall(txt)
            if not cs:
                errors.append(f"S2 第 {i} 張有重點沒有 [wiki:slug]：「{txt[:40]}」")
            for c in cs:
                if c not in pages:
                    errors.append(f"S3 第 {i} 張引用了不存在的頁面 [wiki:{c}]")
                else:
                    cited.add(c)
        body = CITE_RE.sub("", s["text"])
        cited_text = norm_num("".join(pages[c] for c in cited))
        for m in NUM_RE.findall(body):
            if norm_num(m) not in cited_text:
                errors.append(f"S4 第 {i} 張的數字「{m.strip()}」在引用的 wiki 頁面中找不到（引用：{', '.join(sorted(cited)) or '無'}）")

    rendered = None
    if not args.no_render:
        rendered, probs = render_check(deck)
        errors += probs

    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M") if TZ else datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [f"# 簡報程式檢查（{now}）", "", f"- 檔案：{deck}", f"- 張數：{len(slides)}",
           f"- 渲染檢查：{'略過' if args.no_render else ('已執行' if rendered is not None else '無法執行')}",
           f"- 錯誤：{len(errors)}", "", "## 錯誤"] + ([f"- {e}" for e in errors] or ["- 無"])
    text = "\n".join(out) + "\n"
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(text, encoding="utf-8")
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
