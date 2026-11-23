#!/usr/bin/env python3
"""Graph 版：證據卡檢查（程式關卡）。

用法：python3 scripts/check_cards.py slides/v3_graph/cards.json [--wiki wiki] [--report slides/v3_graph/cards_check.md]

證據卡格式（JSON list）：
  {"id": "c01", "page": "causes", "quote": "<從該 wiki 頁逐字摘錄的句子>",
   "source": "IBM", "kind": "fact|opinion|example-real|example-demo|example-hypo", "plain": "<給大學生的白話說法>"}

檢查：
- K1 id 不重複
- K2 page 存在於 wiki/
- K3 quote 必須能在該頁「逐字」找到（忽略 markdown 符號與空白差異）
- K4 kind 必須是規定的值；source 不可空白
有錯誤時 exit code = 1。
"""
import argparse
import json
import re
import sys
from pathlib import Path

KINDS = {"fact", "opinion", "example-real", "example-demo", "example-hypo"}


def norm(t: str) -> str:
    t = re.sub(r"\[\[([^\]|]+)(\|[^\]]*)?\]\]", r"\1", t)
    t = re.sub(r"[*`#>|]", "", t)
    t = re.sub(r"^\s*-\s+", "", t, flags=re.M)
    return re.sub(r"\s+", "", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cards")
    ap.add_argument("--wiki", default="wiki")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    wiki = Path(a.wiki)
    cards = json.loads(Path(a.cards).read_text(encoding="utf-8"))
    errors, seen = [], set()
    for c in cards:
        cid = c.get("id", "?")
        if cid in seen:
            errors.append(f"K1 id 重複：{cid}")
        seen.add(cid)
        p = wiki / f"{c.get('page', '')}.md"
        if not p.exists():
            errors.append(f"K2 {cid} 的頁面不存在：{c.get('page')}")
            continue
        if norm(c.get("quote", "")) == "" or norm(c["quote"]) not in norm(p.read_text(encoding="utf-8")):
            errors.append(f"K3 {cid} 的 quote 在 {c['page']}.md 找不到逐字對應：「{c.get('quote', '')[:40]}」")
        if c.get("kind") not in KINDS:
            errors.append(f"K4 {cid} 的 kind 不合法：{c.get('kind')}")
        if not c.get("source"):
            errors.append(f"K4 {cid} 沒有 source")
    out = ["# 證據卡檢查", "", f"- 卡片數：{len(cards)}", f"- 錯誤：{len(errors)}", "", "## 錯誤"] + ([f"- {e}" for e in errors] or ["- 無"])
    text = "\n".join(out) + "\n"
    if a.report:
        Path(a.report).write_text(text, encoding="utf-8")
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
