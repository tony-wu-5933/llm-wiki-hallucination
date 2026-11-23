# log.md

依時間只增不改。格式見 AGENTS.md 3.4。

## [2026-11-23 11:24] interview | 需求訪談
- 依「先討論、後生成」進行 10 題訪談（紀錄：interview.md），使用者確認需求摘要。

## [2026-11-23 12:00] setup | AGENTS.md、資料夾、lint 腳本
- 依需求摘要產生 AGENTS.md、CLAUDE.md、wiki/ 結構與 scripts/lint.py。
- raw/ 放入 5 篇原文 PDF，以 pdftotext -layout 轉成 raw/text/*.txt。

## [2026-11-23 12:00] lint | 空 wiki 試跑
- lint 第一次試跑就誤報 L2：index.md 說明文字中的格式範例 `[[slug]]` 被當成連結。
- 修正 scripts/lint.py：解析前先移除程式碼區塊與行內程式碼；時間改用 Asia/Taipei。重跑通過。
