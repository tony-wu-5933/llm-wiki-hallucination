#!/usr/bin/env python3
"""Graph 版：把已通過忠實度檢查的逐頁稿，用固定模板組成 HTML。

用法：python3 scripts/render_deck.py slides/v3_graph [--wiki wiki]
讀：<dir>/cards.json、<dir>/drafts/slide_XX.json（依檔名排序）
寫：<dir>/index.html

這個節點「不能改任何一個字」：只把稿件中的文字放進模板，不生成、不改寫內容。
每個重點元素的 data-src 由它引用的證據卡自動換算成 wiki 頁面。

逐頁稿格式（JSON）：
{
  "type": "title" | "content" | "summary",
  "title": "投影片標題",
  "core": {"text": "核心重點", "cards": ["c01"]},          # content 必填
  "blocks": [ ...見下方... ]
}
block 類型：
  {"type": "bullets", "items": [{"text": "...", "cards": ["c01"]}]}
  {"type": "chat", "label": "真實事件", "q": {"text": "...", "cards": []},
       "a": {"text": "...", "cards": [], "wrong": ["要標紅的子字串"]}, "note": {"text": "...", "cards": []}}
  {"type": "chats", "items": [<chat>, <chat>]}
  {"type": "bar", "title": "...", "label": "...", "unit": "%", "series": ["A", "B"],
       "groups": [{"name": "棄答率", "values": [52, 1]}], "cards": ["c10"]}
  {"type": "flow", "label": "假設情境", "steps": [{"text": "...", "cards": []}]}
  {"type": "columns", "cols": [{"head": "IBM", "items": [{"text": "...", "cards": []}]}]}
  {"type": "callout", "tag": "注意", "text": "...", "cards": []}
  {"type": "icon", "name": "warn|search|book|chat|loop|shield"}
"""
import argparse
import html
import json
import sys
from pathlib import Path

PAGE_NAMES = {
    "overview": "總覽", "definition": "定義", "taxonomy": "分類", "causes": "成因", "examples": "例子",
    "impact": "影響", "detection": "偵測", "mitigation": "減少方法", "myths": "迷思",
    "sources/ibm": "IBM 摘要", "sources/openai": "OpenAI 摘要", "sources/anthropic": "Anthropic 摘要",
    "sources/ji2023": "Ji et al. 摘要", "sources/huang2023": "Huang et al. 摘要",
}
COLORS = ["#3b82f6", "#f97316", "#10b981", "#a855f7", "#ef4444"]

ICONS = {
    "warn": '<circle cx="40" cy="40" r="34" fill="#fff4d6" stroke="#f59e0b" stroke-width="4"/><rect x="36" y="18" width="8" height="30" rx="4" fill="#f59e0b"/><circle cx="40" cy="58" r="5" fill="#f59e0b"/>',
    "search": '<circle cx="34" cy="34" r="20" fill="#e0f2fe" stroke="#3b82f6" stroke-width="6"/><line x1="49" y1="49" x2="68" y2="68" stroke="#3b82f6" stroke-width="8" stroke-linecap="round"/>',
    "book": '<rect x="10" y="16" width="28" height="48" rx="4" fill="#dcfce7" stroke="#10b981" stroke-width="4"/><rect x="42" y="16" width="28" height="48" rx="4" fill="#dcfce7" stroke="#10b981" stroke-width="4"/>',
    "chat": '<rect x="8" y="12" width="52" height="36" rx="12" fill="#ede9fe" stroke="#a855f7" stroke-width="4"/><path d="M22 48 L18 64 L36 48" fill="#ede9fe" stroke="#a855f7" stroke-width="4"/><circle cx="24" cy="30" r="4" fill="#a855f7"/><circle cx="34" cy="30" r="4" fill="#a855f7"/><circle cx="44" cy="30" r="4" fill="#a855f7"/>',
    "loop": '<path d="M20 40 A20 20 0 1 1 40 60" fill="none" stroke="#f97316" stroke-width="7" stroke-linecap="round"/><path d="M40 52 L40 68 L54 60 Z" fill="#f97316"/>',
    "shield": '<path d="M40 8 L68 20 L64 48 C60 62 50 70 40 74 C30 70 20 62 16 48 L12 20 Z" fill="#dcfce7" stroke="#10b981" stroke-width="4"/><path d="M28 40 L37 50 L54 30" fill="none" stroke="#10b981" stroke-width="6" stroke-linecap="round"/>',
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;background:#eef2ff;color:#1f2937}
.deck{width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
section.slide{display:none;position:relative;width:1280px;height:720px;max-width:100vw;max-height:100vh;background:#fff;
  border-radius:0;padding:40px 56px 48px;overflow:hidden;background-image:radial-gradient(circle at 100% 0,#fef3c7 0,transparent 260px),radial-gradient(circle at 0 100%,#e0f2fe 0,transparent 300px)}
section.slide.active{display:flex;flex-direction:column}
h1{font-size:60px;line-height:1.2;font-weight:900;color:#1e1b4b}
h2{font-size:36px;font-weight:900;color:#1e1b4b;margin-bottom:14px;display:flex;align-items:center;gap:14px}
h2 .no{display:inline-flex;width:46px;height:46px;border-radius:50%;background:#6366f1;color:#fff;font-size:24px;align-items:center;justify-content:center;flex:none}
.core{font-size:27px;font-weight:700;background:#eef2ff;border-left:8px solid #6366f1;border-radius:14px;padding:12px 20px;margin-bottom:18px;line-height:1.45}
.body{flex:1;display:flex;gap:22px;min-height:0;align-items:flex-start}
.body.stack{flex-direction:column;gap:14px}
.col{flex:1;display:flex;flex-direction:column;gap:14px;min-width:0}
ul.points{list-style:none;display:flex;flex-direction:column;gap:12px}
ul.points li{font-size:23px;line-height:1.5;background:#f8fafc;border-radius:14px;padding:10px 16px 10px 44px;position:relative}
ul.points li::before{content:"";position:absolute;left:16px;top:20px;width:12px;height:12px;border-radius:50%;background:#6366f1}
.chatbox{background:#f8fafc;border:2px solid #e2e8f0;border-radius:20px;padding:14px 16px;display:flex;flex-direction:column;gap:10px;flex:1;min-width:0}
.tag{display:inline-block;font-size:17px;font-weight:700;padding:3px 12px;border-radius:999px;background:#fef3c7;color:#92400e;align-self:flex-start}
.tag.real{background:#dcfce7;color:#166534}
.bubble{font-size:22px;line-height:1.45;padding:10px 16px;border-radius:18px;max-width:92%}
.bubble.q{align-self:flex-end;background:#6366f1;color:#fff;border-bottom-right-radius:4px}
.bubble.a{align-self:flex-start;background:#fff;border:2px solid #e2e8f0;border-bottom-left-radius:4px}
.bubble.a .who{display:block;font-size:15px;color:#64748b;font-weight:700}
.bubble.q .who{display:block;font-size:15px;color:#e0e7ff;font-weight:700}
mark.wrong{background:#fecaca;color:#b91c1c;font-weight:700;padding:0 3px;border-radius:4px}
.bubble.note{align-self:stretch;max-width:100%;background:#ecfdf5;border:2px dashed #10b981;font-size:20px}
.columns{display:flex;gap:16px;width:100%}
.columns .c{flex:1;background:#f8fafc;border-radius:18px;padding:14px;border-top:8px solid #6366f1;display:flex;flex-direction:column;gap:10px}
.columns .c h3{font-size:24px;font-weight:900}
.columns .c .point{font-size:21px;line-height:1.45;background:#fff;border-radius:12px;padding:8px 12px}
.callout{display:flex;gap:12px;align-items:center;background:#fff7ed;border:2px solid #fdba74;border-radius:16px;padding:12px 16px;font-size:22px;line-height:1.45;width:100%}
.callout b{flex:none;background:#f97316;color:#fff;border-radius:999px;padding:2px 12px;font-size:18px}
.flow{display:flex;align-items:stretch;gap:10px;width:100%}
.flow .point{flex:1;font-size:21px;line-height:1.4;background:#fff7ed;border:2px solid #fdba74;border-radius:16px;padding:12px;text-align:center;display:flex;align-items:center;justify-content:center}
.flow .arr{flex:none;align-self:center;font-size:34px;color:#f97316;font-weight:900}
.figure{background:#fff;border-radius:18px;border:2px solid #e2e8f0;padding:10px 14px;width:100%}
.figure .ftitle{font-size:20px;font-weight:700;margin-bottom:4px}
.src{position:absolute;right:28px;bottom:14px;font-size:15px;color:#64748b;background:#f1f5f9;border-radius:999px;padding:3px 12px}
.pageno{position:absolute;left:28px;bottom:14px;font-size:15px;color:#94a3b8}
.title-wrap{flex:1;display:flex;align-items:center;gap:40px}
.subtitle{font-size:26px;color:#475569;margin-top:18px;line-height:1.5}
.nav{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:9}
.nav button{border:0;background:#6366f1;color:#fff;border-radius:999px;width:40px;height:40px;font-size:20px;cursor:pointer;opacity:.6}
@media print{.nav{display:none}section.slide{display:flex!important;page-break-after:always}}
"""

JS = """
const S=[...document.querySelectorAll('section.slide')];let i=0;
function show(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,j)=>s.classList.toggle('active',j===i));history.replaceState(null,'','#'+(i+1));}
document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key))show(i+1);if(['ArrowLeft','PageUp'].includes(e.key))show(i-1);if(e.key==='Home')show(0);if(e.key==='End')show(S.length-1);});
document.getElementById('prev').onclick=()=>show(i-1);document.getElementById('next').onclick=()=>show(i+1);
show((parseInt(location.hash.slice(1))||1)-1);
"""


class R:
    def __init__(self, cards):
        self.cards = {c["id"]: c for c in cards}
        self.used = []

    def src(self, ids):
        pages = []
        for cid in ids or []:
            if cid not in self.cards:
                raise SystemExit(f"稿件引用了不存在的證據卡：{cid}")
            p = self.cards[cid]["page"]
            if p not in pages:
                pages.append(p)
        self.used += pages
        return html.escape(",".join(pages))

    @staticmethod
    def esc(t):
        return html.escape(t or "")

    def marked(self, a):
        t = self.esc(a.get("text"))
        for w in a.get("wrong", []):
            ew = self.esc(w)
            if ew not in t:
                raise SystemExit(f"要標紅的「{w}」不在回答文字中")
            t = t.replace(ew, f'<mark class="wrong">{ew}</mark>', 1)
        return t

    def chat(self, b):
        cls = "tag real" if "真實" in b.get("label", "") else "tag"
        out = [f'<div class="chatbox"><span class="{cls}">{self.esc(b.get("label"))}</span>']
        q, a = b.get("q"), b.get("a")
        if q:
            out.append(f'<div class="bubble q" data-src="{self.src(q.get("cards"))}"><span class="who">{self.esc(q.get("who", "使用者"))}</span>{self.esc(q["text"])}</div>')
        if a:
            out.append(f'<div class="bubble a" data-src="{self.src(a.get("cards"))}"><span class="who">{self.esc(a.get("who", "AI"))}</span>{self.marked(a)}</div>')
        n = b.get("note")
        if n:
            out.append(f'<div class="bubble note" data-src="{self.src(n.get("cards"))}">{self.esc(n["text"])}</div>')
        out.append("</div>")
        return "".join(out)

    def bar(self, b):
        series, groups, unit = b["series"], b["groups"], b.get("unit", "")
        W, H, pad = 640, 300, 40
        mx = max(v for g in groups for v in g["values"]) or 1
        gw = (W - pad * 2) / len(groups)
        bw = min(70, gw / (len(series) + 1))
        parts = [f'<svg viewBox="0 0 {W} {H + 60}" width="100%" role="img" aria-label="{self.esc(b.get("title"))}">',
                 f'<line x1="{pad}" y1="{H}" x2="{W - pad}" y2="{H}" stroke="#94a3b8" stroke-width="2"/>']
        for gi, g in enumerate(groups):
            x0 = pad + gi * gw + (gw - bw * len(series)) / 2
            for si, v in enumerate(g["values"]):
                h = (H - 40) * v / mx
                x = x0 + si * bw
                parts.append(f'<rect x="{x:.1f}" y="{H - h:.1f}" width="{bw - 8:.1f}" height="{h:.1f}" rx="6" fill="{COLORS[si % 5]}"/>')
                parts.append(f'<text x="{x + (bw - 8) / 2:.1f}" y="{H - h - 8:.1f}" text-anchor="middle" font-size="20" font-weight="700" fill="#1f2937">{v}{self.esc(unit)}</text>')
            parts.append(f'<text x="{pad + gi * gw + gw / 2:.1f}" y="{H + 30}" text-anchor="middle" font-size="20" fill="#334155">{self.esc(g["name"])}</text>')
        for si, s in enumerate(series):
            parts.append(f'<rect x="{pad + si * 260}" y="{H + 42}" width="16" height="16" rx="3" fill="{COLORS[si % 5]}"/><text x="{pad + 22 + si * 260}" y="{H + 56}" font-size="18" fill="#334155">{self.esc(s)}</text>')
        parts.append("</svg>")
        lab = f'<span class="tag">{self.esc(b["label"])}</span>' if b.get("label") else ""
        return f'<div class="figure point" data-src="{self.src(b.get("cards"))}"><div class="ftitle">{self.esc(b.get("title"))} {lab}</div>{"".join(parts)}</div>'

    def flow(self, b):
        out = [f'<div class="body stack" style="width:100%">']
        if b.get("label"):
            out.append(f'<span class="tag">{self.esc(b["label"])}</span>')
        out.append('<div class="flow">')
        for k, s in enumerate(b["steps"]):
            if k:
                out.append('<span class="arr">→</span>')
            out.append(f'<div class="point" data-src="{self.src(s.get("cards"))}">{self.esc(s["text"])}</div>')
        out.append("</div></div>")
        return "".join(out)

    def columns(self, b):
        out = ['<div class="columns">']
        for k, c in enumerate(b["cols"]):
            out.append(f'<div class="c" style="border-top-color:{COLORS[k % 5]}"><h3>{self.esc(c["head"])}</h3>')
            if c.get("sub"):
                out.append(f'<span class="tag">{self.esc(c["sub"])}</span>')
            for it in c["items"]:
                out.append(f'<div class="point" data-src="{self.src(it.get("cards"))}">{self.esc(it["text"])}</div>')
            out.append("</div>")
        out.append("</div>")
        return "".join(out)

    def block(self, b):
        t = b["type"]
        if t == "bullets":
            return '<ul class="points">' + "".join(f'<li data-src="{self.src(it.get("cards"))}">{self.esc(it["text"])}</li>' for it in b["items"]) + "</ul>"
        if t == "chat":
            return self.chat(b)
        if t == "chats":
            return '<div class="columns">' + "".join(self.chat(c) for c in b["items"]) + "</div>"
        if t == "bar":
            return self.bar(b)
        if t == "flow":
            return self.flow(b)
        if t == "columns":
            return self.columns(b)
        if t == "callout":
            return f'<div class="callout point" data-src="{self.src(b.get("cards"))}"><b>{self.esc(b.get("tag", "注意"))}</b><span>{self.esc(b["text"])}</span></div>'
        if t == "icon":
            return f'<svg viewBox="0 0 80 80" width="120" height="120" style="flex:none">{ICONS[b["name"]]}</svg>'
        raise SystemExit(f"未知的 block 類型：{t}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    a = ap.parse_args()
    d = Path(a.dir)
    cards = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    r = R(cards)
    drafts = sorted((d / "drafts").glob("slide_*.json"))
    sections = []
    n = len(drafts)
    no = 0
    for k, f in enumerate(drafts, 1):
        s = json.loads(f.read_text(encoding="utf-8"))
        r.used = []
        typ = s.get("type", "content")
        inner = []
        if typ == "title":
            blocks = "".join(r.block(b) for b in s.get("blocks", []))
            inner.append(f'<div class="title-wrap"><div><span class="tag">給用過 ChatGPT 的你</span><h1>{r.esc(s["title"])}</h1>'
                         f'<div class="subtitle">{r.esc(s.get("subtitle", ""))}</div></div>{blocks}</div>')
            attr = ' data-type="title"'
        else:
            if typ == "content":
                no += 1
                head = f'<span class="no">{no}</span>'
            else:
                head = '<span class="no">★</span>'
            inner.append(f"<h2>{head}{r.esc(s['title'])}</h2>")
            if s.get("core"):
                inner.append(f'<div class="core" data-src="{r.src(s["core"].get("cards"))}">{r.esc(s["core"]["text"])}</div>')
            layout = s.get("layout", "stack")
            if layout == "row":
                inner.append('<div class="body">' + "".join(f'<div class="col">{r.block(b)}</div>' if b["type"] != "icon" else r.block(b) for b in s.get("blocks", [])) + "</div>")
            else:
                inner.append('<div class="body stack">' + "".join(r.block(b) for b in s.get("blocks", [])) + "</div>")
            attr = ' data-type="summary"' if typ == "summary" else ""
        pages = list(dict.fromkeys(r.used))
        srclabel = "出處：Wiki／" + "、".join(PAGE_NAMES.get(p, p) for p in pages) if pages else ""
        foot = f'<span class="pageno">{k} / {n}</span>' + (f'<span class="src">{r.esc(srclabel)}</span>' if srclabel else "")
        sections.append(f'<section class="slide"{attr} data-draft="{f.name}">{"".join(inner)}{foot}</section>')
    doc = (f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>LLM 幻覺是什麼？</title><style>{CSS}</style></head><body><div class="deck">{"".join(sections)}</div>'
           f'<div class="nav"><button id="prev" aria-label="上一張">‹</button><button id="next" aria-label="下一張">›</button></div>'
           f'<script>{JS}</script></body></html>')
    (d / "index.html").write_text(doc, encoding="utf-8")
    print(f"已組成 {n} 張 → {d / 'index.html'}")


if __name__ == "__main__":
    sys.exit(main())
