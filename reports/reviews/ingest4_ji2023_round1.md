# 審查報告：ingest 4（Ji et al.）第 1 輪

- 結論：**不通過**（有 R1 2 項、R2 3 項，都是小幅修改，沒有數字錯誤）

數字核對結果：62%（WIKIBIO 的第一句含有 infobox 沒有的資訊，第 3.1 節）、25%（用 ROUGE、BLEU、METEOR 評估的頂尖摘要系統所產生的摘要，第 4 節）、41%→21%（GPT-3 用 RLHF 微調成 InstructGPT，closed-domain 任務，第 13.3.2 節），三個數字和適用範圍都與原文一致。

## R1 問題

| 頁面 | 句子 | 原文怎麼說 | 建議修改 |
|---|---|---|---|
| mitigation.md（Ji et al. 表格）；sources/ji2023.md 第 8 點 | 方法類別「先推理、再驗證」（sources 頁寫「推理驗證」），說明為「例如 Chain-of-Verification：先寫初稿，再列出查證問題……」 | 第 13.3.2 節的類別是 "Chain-of-Thought and Variants"：「encourage LLMs to reason prior to arriving at a final reply, which improves performance and reduces hallucinations by leveraging the model's internal knowledge」。CoVe 只是其中一個例子，同類的 SPP（一個 LLM 扮演多個角色、多輪自我合作）並沒有驗證步驟。類別名稱寫成「再驗證」，會讓人以為這類方法都有驗證步驟，把單一例子推成了整個類別 | 類別改成「先推理、再回答（Chain-of-Thought 及其變形）」，說明改為「讓模型先推理再給最終答案；例如 Chain-of-Verification 會先寫初稿，再列出查證問題、各自獨立回答，最後產生驗證過的回答」。sources 頁的「推理驗證」也改成「先推理再回答」 |
| detection.md（LLM 偵測方法表，「需要參考答案」那一列） | 「因為常見知識容易被記住，這類題庫多半考少見的冷門知識，或專門蒐集容易引發幻覺的題目」 | 這段描述的是 13.2.1 節底下的 "Human-annotated Hallucination Benchmarks"（人工標註的題庫）：「examining low frequency, long-tailed knowledge becomes a primary focus of these hallucination benchmarks」。同一節還有 "Automated Hallucination Benchmarking"，是把維基百科、新聞自動轉成題目，或自動從網路檢索證據，並沒有說這類方法「多半考冷門知識」。頁面把一個子類別的特徵寫成整個 reference-dependent 類別的特徵 | 改成「其中人工建立的題庫，因為常見知識容易被記住，多半考少見的冷門知識，或專門蒐集容易引發幻覺的題目；也有自動產生題目或自動上網找證據的做法」 |

## R2 問題

| 頁面 | 句子 | 原文怎麼說 | 建議修改 |
|---|---|---|---|
| definition.md「定義的基準：各來源不同」表格的 Ji et al. 那一列；overview.md 第 1 點 | 表格：「無意義，或不忠於所提供的來源；……」。overview：「Ji et al. 則把幻覺定義為『無意義，或不忠於所提供來源』的內容」 | 第 2 節的定義是 NLG 時代的版本。第 13.1 節明確說 LLM 的幻覺「not only signifies deviations from the source input but also extends to deviations from training data」，並說「the reference discussed in Section 2.3 includes both the input source and the training data」。這個 wiki 的主題是 LLM 幻覺，比較表和總覽只列第 2 節的基準，會讓讀者以為 Ji et al. 對 LLM 的判斷基準只有「提供的來源」，比較時沒有完整呈現 Ji et al. 的說法（正文第 18 行有寫，但表格和總覽沒有） | 表格的 Ji et al. 那一列補上：「對 LLM 而言（第 13 節），基準不只是輸入的來源，也包括訓練資料」。overview 第 1 點改成：「Ji et al. 把幻覺定義為『無意義，或不忠於所提供來源』的內容；對 LLM 則擴大為也包括偏離訓練資料，並指出……」 |
| detection.md（LLM 偵測方法表，「不需要參考答案」那一列） | 「一種是看模型給每個 token 的機率（不確定的地方常含幻覺）」 | 13.2.2 節：「This type of method **assumes** that LLMs assign high probabilities to tokens that they are confident of, and low probabilities to uncertain tokens, which usually contain hallucinated information.」這是方法本身的「假設」，頁面把它寫成了事實 | 改成「一種是看模型給每個 token 的機率（這類方法假設模型不確定的 token 常含幻覺）」 |
| causes.md（「來自訓練與生成」表，parametric knowledge bias 那一列） | 「有研究發現模型會優先使用這些知識，而不是輸入的資料，因而在輸出中加入多餘的內容」 | 第 3.2 節：Longpre et al. 發現模型會優先使用參數知識（這是研究發現，頁面寫法正確）；但後果的寫法是「models that favor generating output with their parametric knowledge … **can result in** the hallucination of excess information in the output」。頁面把「can」寫成必然的結果 | 改成「……而不是輸入的資料，這可能讓輸出出現多餘的幻覺內容」 |

## R3 提醒

以下內容都在第 1–5 節或第 13 節之內，與「LLM 幻覺是什麼」相關，對大學生也有用，目前沒有收錄。只是提醒，要不要收由使用者決定。

| 位置 | 內容 | 可能放在哪一頁 |
|---|---|---|
| 13.4.3 | 預訓練資料再大，也不可能涵蓋全世界的知識，所以教模型在答不出來時誠實說「我不知道」很重要，這需要模型準確掌握自己知識的邊界；相關研究仍在早期，現有方法都還不能令人滿意地解決這個問題。這和 mitigation.md「『允許說不知道』三個來源都提到」、definition.md「幻覺能不能避免？」兩處比較直接相關：目前比較只列 IBM、OpenAI、Anthropic，Ji et al. 其實也談到了 | mitigation.md、definition.md 的比較段落 |
| 13.4.4 | Alignment tax：減少幻覺的做法也可能有代價，例如持續做安全微調後 ChatGPT、GPT-4 的表現下降；RAG 在檢索到的證據品質不佳時也可能降低回答品質；作者提醒要避免模型變得過度保守、失去創意 | mitigation.md |
| 13.4.2 | 長尾和低資源的領域仍是重大挑戰，包括低資源語言（對高資源語言有效的方法不一定適用）和較新的資料（新近資料也算長尾、低資源） | causes.md 或 impact.md |
| 13.4.5 | 研究界對 LLM 幻覺的理解仍然有限，缺少可靠的理論框架；例如幻覺和模型與資料規模的關係、不同任務幻覺的下限都還沒有答案 | overview.md 或 definition.md |
| 2.2 | 不同任務對幻覺的容忍度不同：摘要和 data-to-text 的容忍度很低；開放式對話容忍度較高，因為除了忠實，還重視讓使用者投入 | definition.md |
| 3.2 | 即使資料集中來源和參考答案幾乎沒有落差，幻覺仍會發生（Parikh et al.），所以模型的訓練與建模選擇是另一個成因；另外也有研究指出，模型在某種程度上能察覺自己正在產生幻覺 | causes.md |
| 13.2.1 | 自動化的偵測做法：根據要查證的內容產生搜尋查詢，自動上網找證據，再判斷是否有幻覺（類似自動事實查核），和學生自己查證 AI 回答的做法相近 | detection.md |
| 13.2.1 | Known-Unknown 等題庫測試模型能不能察覺「沒有確定答案的問題」（例如「如果宇宙始於大爆炸，那之前存在什麼？」） | detection.md |
| 第 1 節註腳 2 | 「hallucination」這個詞最早出現在電腦視覺，原本帶有正面意義（例如超解析度、影像修補），是被利用而不是被避免的 | definition.md（名稱由來） |

## 其他檢查

**examples.md 的標示。** Ji et al. 的四個例子標示都正確。伊波拉疫苗和 COVID-19 臨床試驗兩例出自 Table 1，原文稱為 "examples"，標成「論文表格中的示範例子」正確，intrinsic／extrinsic 的歸類也與原文一致。「全球暖化是騙局」是 TruthfulQA 題目和 GPT-3 的實際回答，標成「Benchmark 中的題目與模型回答」可以接受；原文沒有把它歸成 intrinsic 或 extrinsic，「原文未歸類」也正確。「吐出個人資料」是 Carlini et al. 的研究結果，標成「研究發現」正確，「Ji et al. 視為幻覺，因為不在輸入來源中」與第 1 節一致。

**比較段落。** detection.md 說 Anthropic 的 Best-of-N 和 Ji et al. 的 consistency-based 方法做法相同，對照兩份原文都成立。mitigation.md 說 Ji et al. 把 RAG 視為減少幻覺的方法並指出其挑戰，原文是 "a popular method used to mitigate hallucination"，之後列出三項挑戰，一致。taxonomy.md 的並列表、causes.md 的「不同來源的說法」中與 Ji et al. 相關的句子，都與原文一致。

**sources/ji2023.md。** 作者、版本（arXiv v7，2024-07-14）、第 13 節於 2024 年 1 月更新、取用範圍，都與原文一致。唯一的問題是第 8 點的「推理驗證」，已列在 R1。
