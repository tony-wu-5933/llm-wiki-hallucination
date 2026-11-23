---
name: slides-graph
description: 用 Graph 方式，只根據 wiki/ 產生「LLM 幻覺是什麼」的教學 HTML 簡報：先做證據卡，逐頁稿只能引用證據卡，逐頁審查只退回出錯那頁，用固定模板組 HTML。
---

# slides-graph：Graph 版教學簡報流程

設計依據：Loop 版（`.agents/skills/slides-loop/SKILL.md`）的觀察。Loop 每輪都要整份重看、修一處就重跑整份（大圈）；而且剩下的錯誤多半出在「一句話離開了它的出處」。Graph 版把檢查往前移到「證據卡」，錯了只退回那一頁（小圈）。
內容限制（只用 wiki、不自己下結論、保留語氣、標明誰說的、並列矛盾、例子標真假、對讀者友善）與版面規格，都沿用 slides-loop 的「限制」一節。

產出位置：`slides/v3_graph/`

## 節點與連線

```
檢索 Wiki ─→ 覆蓋率關卡 ─不過→ 回檢索
              │過
              ▼
           證據卡 ─→ check_cards.py ─不過→ 回證據卡（最多 3 輪）
              │過
              ▼
         大綱（人確認）─要改→ 回大綱
              │確認
              ▼
         逐頁稿 drafts/slide_XX.json（只能引用證據卡）
              │
              ▼
         逐頁忠實度審查（新對話）─某頁退回→ 只重寫那一頁（每頁最多 3 輪）
              │全部通過
              ▼
         render_deck.py（固定模板，不能改任何字）
              │
              ▼
         check_slides.py（張數、出處、數字、核心重點、1280×720 不溢出）─不過→ 回出錯那頁的逐頁稿
              │過
              ▼
         交件前確認（人）
```

## 各節點規格

| 節點 | 輸入 | 輸出 | 完成標準 |
|---|---|---|---|
| 檢索 Wiki | `wiki/` | 要用的頁面與段落 | 只讀 wiki，不讀 raw |
| 證據卡 | 檢索結果 | `cards.json`：`id, page, source, kind, quote, plain` | `scripts/check_cards.py` 0 錯誤：quote 能在該頁逐字找到；kind 為 fact／opinion／example-real／example-demo／example-hypo |
| 覆蓋率關卡 | `outline.md`、`cards.json` | `coverage.md` | 每張內容頁至少 2 張卡；5 個來源都有被引用；大綱用到的卡都存在 |
| 大綱（人確認） | 證據卡 | `outline.md`：每張的標題、核心重點、要用的卡 | 使用者確認 |
| 逐頁稿 | 大綱、證據卡 | `drafts/slide_XX.json`（格式見 `scripts/render_deck.py`） | 每段文字都有 `cards`，文字只能改寫自那些卡的 quote／plain |
| 逐頁忠實度審查 | 逐頁稿、證據卡、wiki | `review_round<N>.md`，每頁「通過／退回」 | F1 無依據、F2 不忠實為 0；F4 只提醒。審查者不可以是寫稿的同一個對話 |
| 組 HTML | 逐頁稿、證據卡 | `index.html` | `scripts/render_deck.py`；data-src 由卡片自動換算成 wiki 頁面 |
| 渲染檢查 | `index.html` | `render_check_round<N>.md` | `scripts/check_slides.py` 0 錯誤 |

## 剎車

- 每個關卡最多 3 輪；仍不通過就停下，交出目前版本與最後一輪報告。
- 退回只重做出錯的那一頁，其他頁不動。
- 每個節點的結果記入 `wiki/log.md`。
