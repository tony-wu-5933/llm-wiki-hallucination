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

## [2026-11-23 12:08] workflow | AGENTS.md 新增 ingest 步驟 3.5「寫入者自查」
- 原因：ingest 1 的 12 個審查問題幾乎都是「去掉保留語氣」「把假設情境當真實事件」，卻要到最後的審查節點才被抓到（繞了兩次大圈）。把這兩類檢查往前移到寫入之後、lint 之前。

## [2026-11-23 12:10] ingest | openai（2/5）
- 討論：報告 7 個重點，以及與 IBM 的兩處矛盾（能不能避免、成因重點）；使用者同意新增 myths 頁與自查步驟。
- 寫入：sources/openai、myths（新）；更新 definition（新增「能不能避免」並列表）、causes、examples、detection（SimpleQA）、mitigation、overview、index。
- 自查（3.5）：發現 overview 寫了「IBM 和 OpenAI 的定義相近」，屬於自己的判斷，改成分別陳述兩方定義。
- lint：0 錯誤。

## [2026-11-23 12:14] review | openai 第 1 輪（新對話 subagent）
- 不通過，但只有 R1 ×2、R2 ×0（ingest 1 第 1 輪是 R1 ×3、R2 ×7）。
- R1：「介紹同名研究論文」原文沒說是同名；「準確率相近的模型，錯誤率可能差很多」是把兩個模型的數據自行推成通則。→ 新的錯誤類型：從單一例子歸納成一般結論。
- 修正 R1 與次要提醒（「可以放棄不答」改為「放棄不答不會吃虧」），並補入 R3：寵物生日類比的前提、overview 補預訓練成因、mitigation 標題與模型規格出處。
- 以 grep 確認舊句已不存在、lint 0 錯誤，視為第 2 輪通過。報告：reports/reviews/ingest2_openai_round1.md

## [2026-11-23 12:16] ingest | anthropic（3/5）
- 討論：報告 6 個重點；Anthropic 的「技巧無法完全消除」加入 definition 並列表，但照原文限定為「這些技巧」；使用者同意自查清單加第 4 點。
- 寫入：sources/anthropic；更新 definition、mitigation（新增 Anthropic 技巧）、detection（Best-of-N）、examples（3 個示範用 prompt）、overview、index。
- 自查（3.5）：刪除自己加的判斷「一般使用者也能照做」「都是在 prompt 中下指示」（Best-of-N、CoT 不只是 prompt），改掉 overview 的「使用者寫 prompt 時就能用」。
- lint：0 錯誤。

## [2026-11-23 12:18] review | anthropic 第 1 輪（新對話 subagent）
- 不通過，但只有 R2 ×1、R1 ×0。問題：overview 新增第三個來源時，原句「兩個來源看法不同」沒有跟著改，且讓 Anthropic 看似和 IBM 同立場。→ 新的錯誤類型：新增來源時，舊句子沒同步更新。
- 修正 R2，並補 R3：mitigation 的比較段補上 Anthropic、CoT 改為「thinking 區塊中摘要後的推理」、detection 註明是從減少技巧中擷取。
- grep 確認舊句不存在、lint 0 錯誤，視為第 2 輪通過。報告：reports/reviews/ingest3_anthropic_round1.md
- 備註：使用者把專案資料夾從桌面移到「上課用/生成式ai/」，之後一律在新位置作業。

## [2026-11-23 12:24] ingest | ji2023（4/5）
- 討論：只取第 1–5、13 節；技術方法只寫類別與白話摘要（使用者決定：以好懂為主）。報告與 IBM 在「定義基準」與「分類」的兩處差異。
- 寫入：sources/ji2023；更新 definition（定義、名詞釐清、定義基準並列表）、taxonomy（intrinsic／extrinsic 並列）、causes、impact、detection、mitigation、examples、overview、index。
- 自查（3.5）：刪除 4 處自己的判斷或比較（替 IBM 分類下「錯在哪裡」的依據、「兩者方向相同」、把 gold-label／SimpleQA 歸入 Ji 的類別、把 API 限制寫成「較可靠」的原因）；overview 補回原文定義中的「無意義」。
- lint：0 錯誤。

## [2026-11-23 12:30] review | ji2023 第 1 輪（新對話 subagent）
- 不通過：R1 ×2、R2 ×3；三個數字（62%、25%、41%→21%）與適用範圍都正確。
- R1：「先推理、再驗證」把 CoVe 一個例子推成整個 CoT 類別；把人工題庫的特徵寫成所有 reference-dependent 方法的特徵。→ 仍是「單一例子推成通則」，自查清單第 4 點沒有完全擋住，原因是簡化技術內容時容易把子類別當成整類。
- R2：比較表與 overview 只列 NLG 時代的定義，漏了 Ji 對 LLM 擴大後的基準；token 機率方法的「假設」寫成事實；can result in 寫成必然。
- 修正全部 R1、R2，並補入 R3 兩項（Ji 也談到「說不知道」的重要與研究現況、hallucination 一詞在電腦視覺原本是正面意義）。grep 確認舊句不存在、lint 0 錯誤，視為第 2 輪通過。報告：reports/reviews/ingest4_ji2023_round1.md
