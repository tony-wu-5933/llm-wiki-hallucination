---
name: slides-graph
description: 用 Graph 方式，只根據 wiki/ 產生「LLM 幻覺是什麼」的教學 HTML 簡報：先做帶「必須保留的條件」的證據卡，逐頁稿只能引用證據卡，程式與新對話分別把關，錯了只退回那一關、那一頁，最後用固定模板組 HTML。
---

# slides-graph：Graph 版教學簡報流程

流程由使用者設計（節點、人工確認點、退回規則由使用者決定），流程圖：`flow/slides_graph.svg`。

設計依據：
- Loop 版（`.agents/skills/slides-loop/SKILL.md`）每輪都要整份重看，修一處就重跑整份（大圈），而且剩下的錯誤多半出在「一句話離開了它的出處」→ 加入證據卡，錯了只退回那一頁（小圈）。
- Graph 第 1 次執行（2026-11-23）的反思：引文都對得上，錯誤出在「把卡片改寫成投影片文字」時省略主詞、條件與保留語氣 → 證據卡加一欄 `keep`（必須保留的條件），並在 AI 審查之前加一個程式關卡 `check_drafts.py`。

內容限制（只用 wiki、不自己下結論、保留語氣、標明誰說的、並列矛盾、例子標真假、對讀者友善）與版面規格，沿用 slides-loop 的「限制」一節。產出位置：`slides/v3_graph/`。

## 節點

| # | 節點 | 誰做 | 輸出 | 通過標準 | 不通過退回 |
|---|---|---|---|---|---|
| 1 | 檢索 Wiki | AI | 要用的段落 | 只讀 wiki，不讀 raw | — |
| 2 | 寫證據卡 | AI | `cards.json`：`id, page, source, kind, quote, plain, keep` | — | — |
| 3 | 程式檢查證據卡 | 程式 `scripts/check_cards.py` | `cards_check_round<N>.md` | 0 錯誤：K3 quote 能在該頁逐字找到；K5 plain 包含每個 keep；K6 quote 的保留語氣（可能、通常、有時、常常、在很多方面）都列在 keep | 回 2 |
| 4 | 覆蓋率關卡 | 程式 `scripts/check_coverage.py` | `coverage.md` | 每張內容頁 ≥ 2 張卡；5 個來源都有引用；大綱用到的卡都存在 | 回 1 |
| 5 | 大綱確認 | **人** | `outline.md` | 使用者確認 | 重排大綱 |
| 6 | 逐頁寫稿 | AI | `drafts/slide_XX.json` | 每段文字都標引用的卡片 | — |
| 7 | 程式檢查逐頁稿 | 程式 `scripts/check_drafts.py` | `drafts_check_round<N>.md` | 0 錯誤：每段文字保留所引用卡片的 keep；對話框標籤和例子性質一致（真實／示範／假設） | 回 6，只改出錯的頁 |
| 8 | 逐頁審查 | AI（另開新對話，不是寫稿的對話） | `review_round<N>.md`，每頁「通過／退回」 | F1 無依據、F2 不忠實為 0；F4 只提醒 | 回 6，只重寫退回的頁；下一輪只審這些頁 |
| 9 | 固定模板組 HTML | 程式 `scripts/render_deck.py` | `index.html` | 不能改任何字；data-src 由卡片自動換算成 wiki 頁面 | — |
| 10 | 渲染檢查 | 程式 `scripts/check_slides.py` | `render_check_round<N>.md` | 張數 8–15、出處、數字、核心重點與總結、1280×720 不溢出，0 錯誤 | 回 6，只改出錯的頁 |
| 11 | 交件前確認 | **人** | — | 使用者確認 | 依指示退回對應節點 |

## 剎車

- 每個退回最多 3 輪，仍不通過就停下，交出目前版本與最後一輪報告，由人決定。
- 退回只重做出錯的那一頁，其他頁不動。
- 每個節點的結果記入 `wiki/log.md`。
