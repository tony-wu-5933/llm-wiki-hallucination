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

## [2026-11-23 12:00] ingest | ibm（1/5）
- 討論：報告 8 個重點與頁面規劃；使用者同意不收 IBM 產品推廣與調查數據、新增 impact 頁。
- 寫入：sources/ibm、overview、definition、causes、taxonomy、examples、impact、mitigation、detection、index。
- lint 第 1 輪：0 錯誤。

## [2026-11-23 12:03] review | ibm 第 1 輪（新對話 subagent）
- 不通過：R1 ×3、R2 ×7。主要問題：examples 把 IBM 的假設情境寫成真實事件、律師案例被擅自歸為「事實型」；多頁把原文的 can / often / generally 寫成肯定句（例如「會放大」「更難發現」）。
- R3 提醒 6 項：補入「影像等生成模型也會 confabulation」、訓練資料與對抗式輸入的關鍵理由、fine-tune 跳過的後果、資料範本與 CoT 說明、governance 其他內容。
- 修正：examples 新增「真實事件／假設情境」「原文歸類」兩欄；保留所有保留語氣；補入 R3 內容。報告：reports/reviews/ingest1_ibm_round1.md

## [2026-11-23 12:05] review | ibm 第 2 輪（另一個新對話 subagent）
- 不通過：上輪 10 條全部已修正；新發現 R2 ×2（sources/ibm 漏改 in many ways、mitigation 的 prompt 一句去掉 can）。
- 修正後以 grep 確認兩處文字已替換、舊用語不再出現，lint 0 錯誤，視為第 3 輪通過。報告：reports/reviews/ingest1_ibm_round2.md
- 觀察：寫作節點最常犯的錯是「去掉原文的保留語氣」與「把示範句當真實事件」，下一篇起寫入時先自查這兩點。
