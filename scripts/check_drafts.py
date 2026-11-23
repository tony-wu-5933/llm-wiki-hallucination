#!/usr/bin/env python3
"""Graph 版：逐頁稿的程式檢查（在 AI 審查之前）。

用法：python3 scripts/check_drafts.py slides/v3_graph [--report slides/v3_graph/drafts_check.md]
讀：<dir>/cards.json、<dir>/drafts/slide_XX.json

2026-11-23 依 graph 第 1 次執行的反思新增：第 1 次執行時，引文都對得上，
錯誤卻出在「把卡片改寫成投影片文字」時省略主詞、條件與保留語氣。
所以在 AI 審查之前，先用程式確認每段文字都保留了它所引用卡片的 keep（必須保留的條件）。

檢查單位（一個「文字單位」= 一段要對照卡片的文字）：
- core、bullets 的每一項、callout（tag + text）
- columns：欄標題 + 該項文字（欄標題常寫來源名稱，例如「IBM」）
- flow：label + 所有步驟合起來算一個單位（流程圖是一整句話；2026-11-23 第 1 輪後修改）
- chat：label + q + a + note 合起來算一個單位
- bar：只檢查 cards 存在（數字由 check_slides.py 的 S4 檢查）

檢查項目：
- D1 每個文字單位（封面、總結的標題除外）都有引用卡片
- D2 引用的卡片存在
- D3 文字單位包含所引用每張卡片的 keep（必須保留的條件）
- D4 例子標示：引用 example-real 的對話框，label 要有「真實」；example-demo 要有「示範」；example-hypo 要有「假設」
有錯誤時 exit code = 1。
"""
import argparse
import json
import re
import sys
from pathlib import Path


def norm(t):
    return re.sub(r"\s+", "", t or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    d = Path(a.dir)
    cards = {c["id"]: c for c in json.loads((d / "cards.json").read_text(encoding="utf-8"))}
    errors, units = [], 0

    def check(slide, where, text, ids, label=None):
        nonlocal units
        units += 1
        if not ids:
            errors.append(f"D1 {slide} {where}：沒有引用證據卡")
            return
        for cid in ids:
            c = cards.get(cid)
            if c is None:
                errors.append(f"D2 {slide} {where}：卡片 {cid} 不存在")
                continue
            for k in c.get("keep", []):
                if norm(k) not in norm(text):
                    errors.append(f"D3 {slide} {where}：漏了卡片 {cid} 必須保留的「{k}」")
            if label is not None:
                need = {"example-real": "真實", "example-demo": "示範", "example-hypo": "假設"}.get(c["kind"])
                if need and need not in label:
                    errors.append(f"D4 {slide} {where}：引用 {cid}（{c['kind']}），標籤「{label}」沒有標「{need}」")

    def chat(slide, where, b):
        parts = [b.get("label", "")] + [(b.get(k) or {}).get("text", "") for k in ("q", "a", "note")]
        ids = []
        for k in ("q", "a", "note"):
            ids += (b.get(k) or {}).get("cards", [])
        check(slide, where, " ".join(parts), list(dict.fromkeys(ids)), label=b.get("label", ""))

    for f in sorted((d / "drafts").glob("slide_*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        name = f.stem
        if s.get("core"):
            check(name, "core", s["core"]["text"], s["core"].get("cards"))
        for bi, b in enumerate(s.get("blocks", [])):
            t, w = b["type"], f"block{bi + 1}"
            if t == "bullets":
                for i, it in enumerate(b["items"]):
                    check(name, f"{w} 第{i + 1}項", it["text"], it.get("cards"))
            elif t == "callout":
                check(name, w, b.get("tag", "") + " " + b["text"], b.get("cards"))
            elif t == "columns":
                for col in b["cols"]:
                    for i, it in enumerate(col["items"]):
                        check(name, f"{w}「{col['head']}」第{i + 1}項", col["head"] + " " + it["text"], it.get("cards"))
            elif t == "flow":
                ids = []
                for st in b["steps"]:
                    ids += st.get("cards", [])
                check(name, w, b.get("label", "") + " " + " ".join(st["text"] for st in b["steps"]), list(dict.fromkeys(ids)))
            elif t == "chat":
                chat(name, w, b)
            elif t == "chats":
                for i, c in enumerate(b["items"]):
                    chat(name, f"{w} 對話{i + 1}", c)
            elif t == "bar":
                for cid in b.get("cards", []):
                    if cid not in cards:
                        errors.append(f"D2 {name} {w}：卡片 {cid} 不存在")
    out = ["# 逐頁稿程式檢查", "", f"- 文字單位：{units}", f"- 錯誤：{len(errors)}", "", "## 錯誤"] + ([f"- {e}" for e in errors] or ["- 無"])
    text = "\n".join(out) + "\n"
    if a.report:
        Path(a.report).write_text(text, encoding="utf-8")
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
