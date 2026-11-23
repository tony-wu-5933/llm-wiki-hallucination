#!/usr/bin/env python3
"""產生流程圖：flow/slides_graph.svg（簡報 Graph）與 flow/wiki_loop.svg（建 Wiki 的 loop）。
顏色代表誰負責：紫＝AI 生成、粉＝AI 審查（另開新對話）、灰＝程式、橘＝人。右側 ↻ 是不通過時退回哪裡。"""
from html import escape
from pathlib import Path

ROLE = {
    "ai": ("#EEEDFE", "#534AB7", "#3C3489"),
    "review": ("#FBEAF0", "#993556", "#72243E"),
    "code": ("#F1EFE8", "#5F5E5A", "#444441"),
    "human": ("#FAECE7", "#993C1D", "#712B13"),
}
LEGEND = [("ai", "AI 生成"), ("review", "AI 審查（另開新對話）"), ("code", "程式"), ("human", "人")]
FONT = "'Noto Sans TC','Noto Sans CJK TC','Microsoft JhengHei','PingFang TC',sans-serif"


def draw(title, nodes, footer, path):
    W, X, BW, BH, GAP, TOP = 800, 120, 360, 50, 26, 80
    H = TOP + len(nodes) * (BH + GAP) + 110
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         '<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M2 1L8 5L2 9" fill="none" stroke="#888780" stroke-width="1.6" stroke-linecap="round"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{W/2}" y="44" text-anchor="middle" font-size="22" font-weight="700" fill="#2C2C2A">{escape(title)}</text>']
    cx = X + BW / 2
    for i, (role, label, notes) in enumerate(nodes):
        y = TOP + i * (BH + GAP)
        fill, stroke, text = ROLE[role]
        o.append(f'<rect x="{X}" y="{y}" width="{BW}" height="{BH}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        o.append(f'<text x="{cx}" y="{y + BH/2}" text-anchor="middle" dominant-baseline="central" font-size="16" font-weight="700" fill="{text}">{escape(label)}</text>')
        for k, n in enumerate(notes):
            ny = y + BH / 2 + (k - (len(notes) - 1) / 2) * 19
            o.append(f'<text x="{X + BW + 18}" y="{ny}" dominant-baseline="central" font-size="13.5" fill="#444441">{escape(n)}</text>')
        if i < len(nodes) - 1:
            o.append(f'<line x1="{cx}" y1="{y + BH + 2}" x2="{cx}" y2="{y + BH + GAP - 4}" stroke="#888780" stroke-width="1.4" marker-end="url(#a)"/>')
    fy = TOP + len(nodes) * (BH + GAP) + 6
    o.append(f'<text x="{X}" y="{fy}" font-size="13.5" fill="#444441">{escape(footer)}</text>')
    lx = 40
    for role, name in LEGEND:
        fill, stroke, _ = ROLE[role]
        o.append(f'<rect x="{lx}" y="{fy + 34}" width="18" height="18" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        o.append(f'<text x="{lx + 26}" y="{fy + 43}" dominant-baseline="central" font-size="13.5" fill="#444441">{escape(name)}</text>')
        lx += 60 + sum(15 if ord(ch) > 255 else 8 for ch in name)
    o.append("</svg>")
    Path(path).write_text("\n".join(o), encoding="utf-8")


here = Path(__file__).parent

draw("簡報 Graph 流程（slides/v3_graph）", [
    ("ai", "1 檢索 Wiki", []),
    ("ai", "2 寫證據卡（逐字摘錄＋必須保留的條件）", []),
    ("code", "3 程式檢查證據卡", ["↻ 引文找不到、漏了保留語氣 → 回 2"]),
    ("code", "4 覆蓋率關卡", ["↻ 某張投影片卡片太少 → 回 1"]),
    ("human", "5 大綱確認（人）", ["↻ 要改 → 重排大綱"]),
    ("ai", "6 逐頁寫稿（只能引用證據卡）", []),
    ("code", "7 程式檢查逐頁稿", ["↻ 漏了必須保留的條件、", "   例子真假標錯 → 回 6，只改那頁"]),
    ("review", "8 逐頁審查（另開新對話）", ["↻ 只退回出錯的頁 → 回 6，", "   下一輪只審退回的頁"]),
    ("code", "9 固定模板組 HTML", ["這一步不能改任何字"]),
    ("code", "10 渲染檢查", ["↻ 超出畫面 → 回 6，只改那頁"]),
    ("human", "11 交件前確認（人）", []),
], "每個 ↻ 最多 3 輪；還不通過就停下，交給人決定。", here / "slides_graph.svg")

draw("建 Wiki 的 loop（每篇資料跑一次，共 5 篇）", [
    ("ai", "1 讀原文（raw/text）", []),
    ("human", "2 討論（人確認）", ["AI 報告重點、要改哪些頁、", "和既有頁面的矛盾"]),
    ("ai", "3 寫入 Wiki", []),
    ("ai", "4 寫入者自查（5 條清單）", ["從第 2 篇起加入：保留語氣、例子真假、", "誰說的、不推成通則、簡化不走樣"]),
    ("code", "5 lint 腳本", ["↻ 格式錯誤 → 回 3"]),
    ("review", "6 AI 審查（另開新對話）", ["↻ 不忠於原文、矛盾沒並列 → 回 3"]),
    ("code", "7 更新 index、log，git commit", []),
], "每個 ↻ 最多 3 輪；審查常抓到的錯誤，會加進第 4 步的自查清單（檢查往前移）。", here / "wiki_loop.svg")
print("ok")
