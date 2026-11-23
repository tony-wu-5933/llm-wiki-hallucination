# 審查報告：ingest 3（Anthropic）第 1 輪

- 結論：不通過（有 1 項 R2，沒有 R1）

審查範圍：sources/anthropic.md 全文；definition.md、mitigation.md、detection.md、examples.md、overview.md 中來自 Anthropic 的內容，以及提到 Anthropic 的比較段落。比較段落中的 IBM、OpenAI 說法也對照了 ibm.txt、openai.txt（IBM 原文第 69、422 行，OpenAI 原文第 28、56–59、147–148 行）。

逐句核對後沒有問題的部分：
- 定義（definition.md 第 13 行、sources/anthropic.md 第 1 點）：「有時也可能」對應 can sometimes，「可能損害」對應 can undermine，保留語氣都在。
- 三個基本技巧（mitigation.md 第 31–33 行）：「可以大幅減少錯誤資訊」對應 can drastically reduce false information；「超過 20k tokens」數字正確；「找不到就必須撤回」對應 it must retract the claim。
- 四個進階技巧（mitigation.md 第 41–44 行）：「可能發現」對應 can reveal，「可能代表」對應 could indicate，「可以抓出並修正」對應 can catch and correct。
- 結尾提醒（mitigation.md 第 46 行、definition.md 第 21 行）：「大幅減少」對應 significantly reduce，「一定要驗證」對應 Always validate，「無法完全消除」對應 don't eliminate them entirely。
- detection.md 第 26–27 行、overview.md 第 10 行中的 Best-of-N 說明保留了 could indicate 的語氣。
- mitigation.md 第 51 行說「允許說不知道」三個來源都有提到，查證屬實：IBM 原文第 422 行（"if unsure, say you don't know"）、OpenAI 原文第 58–59 行（模型規格）、Anthropic 的基本技巧。
- prompt 範例標示：examples.md 第 15 行寫明「以下三個是 Anthropic 指南中的示範用 prompt，不是幻覺事件」，標示正確。三個範例的關鍵指示（包括「I don't have enough information to confidently assess this」、「No relevant quotes found」、只根據摘錄的引文分析、用空的 [] 標記刪除處）翻譯都沒有改變原意。

## R1 問題

無。

## R2 問題

| 頁面 | 句子 | 原文怎麼說 | 建議修改 |
|---|---|---|---|
| overview.md 第 11 行 | 「能不能完全避免，兩個來源看法不同：IBM 認為……；OpenAI 則認為……；Anthropic 則說它介紹的技巧能大幅減少幻覺，但無法完全消除。」 | 這句話寫「兩個來源」，後面卻列了三個。這樣會讓 Anthropic 看起來像是後來附加、或已被併入 IBM 的立場。三個來源講的其實是不同的事：IBM 談幻覺本身（"hallucinations are inherent to generative AI. They can be reduced but not fully eliminated."，ibm.txt 第 69 行）；OpenAI 說「幻覺不可避免」是迷思（openai.txt 第 147–148 行）；Anthropic 只談它提出的技巧（"although these techniques significantly reduce hallucinations, they don't eliminate them entirely"），沒有表態幻覺本質上能不能避免。 | 改成：「能不能完全避免，各來源說法不同：IBM 認為……；OpenAI 則認為……；Anthropic 沒有討論幻覺本質上能不能避免，只說它介紹的技巧能大幅減少幻覺，但無法完全消除。」這樣跟 definition.md 第 21 行表格的範圍一致。 |

## R3 提醒

| 頁面 | 內容 | 說明 |
|---|---|---|
| mitigation.md 第 52 行（「不同來源的說法」） | 「能否完全消除」這一點只比較了 IBM 和 OpenAI，沒有放 Anthropic | 這不算錯，但 definition.md 和 overview.md 都有放 Anthropic。可以考慮補一句：「Anthropic 只說它的技巧無法完全消除幻覺」，讓三頁一致。 |
| mitigation.md 第 41 行 | 「檢查它的推理過程」 | 原文是 "review the summarized reasoning in the thinking blocks when an answer looks wrong"，檢查的是 thinking blocks 裡的「摘要後的推理」。建議改成「檢查 thinking 區塊中摘要後的推理」，比較精確（意思沒有錯，不影響結論）。 |
| detection.md 第 24–27 行 | 只收了 Best-of-N 和用引用驗證 | 原文中另外兩個進階技巧也有偵測的作用，但沒有收進 detection 頁：Chain-of-thought verification（"This can reveal faulty logic or assumptions."）和 Iterative refinement（"This can catch and correct inconsistencies."）。另外，原文沒有「偵測」這個分類，這些技巧都放在 minimization strategies 底下。可以考慮在本段註明「Anthropic 把這些列為減少幻覺的技巧，此處擷取其中有偵測作用的部分」。 |
| sources/anthropic.md | 沒有收錄文章開頭的目標句 | 原文開頭說本指南的目的是 "minimize hallucinations and ensure Claude's outputs are accurate and trustworthy"，副標題也把三個基本策略概括為 "allowing uncertainty, grounding responses in direct quotes, and verifying claims with citations"。這兩句重要性不高，可以視需要補上。 |
| mitigation.md 第 50 行 | 「多數是在 prompt 中下指示」 | 這是整理者自己的概括，原文沒有這樣說。拿七個技巧來看，基本的三個加上 External knowledge restriction 屬於 prompt 指示；Best-of-N 是多次執行，CoT verification 是開啟 thinking 設定。「多數」這個說法大致成立，不算錯。如果要嚴格只寫原文有的內容，可以改成「多數可以透過 prompt 指示或呼叫方式實作」，或直接刪掉這句概括。 |
