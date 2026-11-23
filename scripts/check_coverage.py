#!/usr/bin/env python3
"""Graph 版：覆蓋率關卡。

用法：python3 scripts/check_coverage.py slides/v3_graph [--report slides/v3_graph/coverage.md]
讀：<dir>/outline.md（表格第 4 欄是證據卡 id，可寫 t01–t08 這種範圍）、<dir>/cards.json

檢查：
- C1 大綱用到的卡片都存在
- C2 每張內容頁（封面、總結除外）至少 2 張證據卡
- C3 5 個來源（IBM、OpenAI、Anthropic、Ji et al.、Huang et al.）都有被引用
- C4 至少引用 3 個 wiki 頁面
有錯誤時 exit code = 1。
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

SOURCES = ["IBM", "OpenAI", "Anthropic", "Ji et al.", "Huang et al."]


def ids_of(cell):
    out = []
    for tok in cell.split():
        m = re.match(r"([a-z])(\d+)–[a-z](\d+)$", tok)
        if m:
            out += [f"{m.group(1)}{i:02d}" for i in range(int(m.group(2)), int(m.group(3)) + 1)]
        elif re.match(r"[a-z]\d+$", tok):
            out.append(tok)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    d = Path(a.dir)
    cards = {c["id"]: c for c in json.loads((d / "cards.json").read_text(encoding="utf-8"))}
    rows = [l for l in (d / "outline.md").read_text(encoding="utf-8").splitlines() if re.match(r"\| \d+ ", l)]
    errors, used, lines = [], set(), []
    last = len(rows)
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        no, title, ids = int(cells[0]), cells[1], ids_of(cells[3])
        miss = [i for i in ids if i not in cards]
        if miss:
            errors.append(f"C1 第 {no} 張引用不存在的卡：{miss}")
        if no not in (1, last) and len(ids) < 2:
            errors.append(f"C2 第 {no} 張證據卡少於 2 張")
        used |= set(i for i in ids if i in cards)
        lines.append(f"- 第 {no} 張「{title}」：{len(ids)} 張卡")
    pages = collections.Counter(cards[i]["page"] for i in used)
    srcs = collections.Counter(cards[i]["source"] for i in used)
    for s in SOURCES:
        if srcs[s] == 0:
            errors.append(f"C3 來源 {s} 沒有被引用")
    if len(pages) < 3:
        errors.append("C4 引用的 wiki 頁面少於 3 頁")
    out = ["# 覆蓋率關卡", ""] + lines + ["", f"- 引用的 wiki 頁面：{dict(pages)}", f"- 各來源卡片數：{dict(srcs)}",
                                        f"- 未使用的卡：{sorted(set(cards) - used) or '無'}", f"- 錯誤：{len(errors)}", "", "## 錯誤"] + ([f"- {e}" for e in errors] or ["- 無"])
    text = "\n".join(out) + "\n"
    if a.report:
        Path(a.report).write_text(text, encoding="utf-8")
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
