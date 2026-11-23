#!/usr/bin/env python3
"""Wiki lint（AGENTS.md 5.1 的 L1–L4）。

用法：python3 scripts/lint.py
結果印出並寫入 reports/lint_latest.md；有錯誤時 exit code = 1。
"""
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
REPORT = ROOT / "reports" / "lint_latest.md"
SPECIAL = {"index", "log"}
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
RAW_RE = re.compile(r"raw/[\w.\-]+\.pdf")


def slug_of(p: Path) -> str:
    return p.relative_to(WIKI).with_suffix("").as_posix()


def main() -> int:
    # 去掉程式碼區塊與行內程式碼，避免把格式範例當成連結
    pages = {slug_of(p): CODE_RE.sub("", p.read_text(encoding="utf-8")) for p in sorted(WIKI.rglob("*.md"))}
    errors, warns = [], []
    # 連結可寫完整 slug（sources/ibm）或只寫檔名（ibm）
    by_name = {}
    for s in pages:
        by_name.setdefault(s.split("/")[-1], []).append(s)

    def resolve(target: str):
        t = target.strip()
        if t in pages:
            return t
        cands = by_name.get(t, [])
        return cands[0] if len(cands) == 1 else None

    inbound = {s: set() for s in pages}
    for s, text in pages.items():
        # L2 斷連結
        for m in LINK_RE.finditer(text):
            r = resolve(m.group(1))
            if r is None:
                errors.append(f"L2 斷連結：{s}.md 連到不存在的 [[{m.group(1)}]]")
            elif r != s and s not in SPECIAL:
                inbound[r].add(s)
        if s in SPECIAL:
            continue
        # L1 來源區塊
        parts = re.split(r"^##\s*來源\s*$", text, flags=re.M)
        if len(parts) < 2:
            errors.append(f"L1 缺少「## 來源」區塊：{s}.md")
        else:
            lines = [l for l in parts[-1].splitlines() if l.strip().startswith("-")]
            if not lines:
                errors.append(f"L1 「## 來源」區塊是空的：{s}.md")
            for l in lines:
                raws = RAW_RE.findall(l)
                if not raws:
                    errors.append(f"L1 來源行沒有寫 raw/ 檔案：{s}.md → {l.strip()}")
                for r in raws:
                    if not (ROOT / r).exists():
                        errors.append(f"L1 來源檔不存在：{s}.md → {r}")

    # L3 孤兒頁
    for s in pages:
        if s in SPECIAL or s == "overview":
            continue
        if not inbound[s]:
            errors.append(f"L3 孤兒頁（沒有任何內容頁連到）：{s}.md")

    # L4 index 完整
    idx = pages.get("index")
    if idx is None:
        errors.append("L4 缺少 wiki/index.md")
    else:
        listed = {}
        for line in idx.splitlines():
            m = re.match(r"\s*-\s*\[\[([^\]]+)\]\]\s*(?:—|-|:)?\s*(.*)$", line)
            if m:
                listed[m.group(1).strip()] = m.group(2).strip()
        for s in pages:
            if s in SPECIAL:
                continue
            key = s if s in listed else (s.split("/")[-1] if s.split("/")[-1] in listed else None)
            if key is None:
                errors.append(f"L4 index.md 沒有列出：{s}")
            elif not listed[key]:
                errors.append(f"L4 index.md 中 {s} 沒有一行摘要")
        for k in listed:
            if resolve(k) is None:
                errors.append(f"L4 index.md 列了不存在的頁面：{k}")

    now = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M")
    content_pages = len([s for s in pages if s not in SPECIAL])
    out = [f"# Lint 報告（{now}）", "", f"- 內容頁數：{content_pages}",
           f"- 錯誤：{len(errors)}", f"- 提醒：{len(warns)}", ""]
    out += ["## 錯誤"] + ([f"- {e}" for e in errors] or ["- 無"])
    out += ["", "## 提醒"] + ([f"- {w}" for w in warns] or ["- 無"])
    text = "\n".join(out) + "\n"
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(text, encoding="utf-8")
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
