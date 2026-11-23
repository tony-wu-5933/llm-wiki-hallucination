# 審查報告：ingest 5（Huang et al.）第 1 輪
- 結論：不通過（2 項 R1、1 項 R2）

整體而言，Huang et al. 的內容大多與原文一致。已逐句對照的部分：第 1 節引言、2.3 節（含表 1）、3.1–3.3 節、4.1 節、5 節開頭與 5.1–5.3 開頭段、6 節開頭與 6.1/6.2 概述、7.2 節。taxonomy 的子類型說明、causes 的三個表、detection、mitigation、RAG 小節，以及 examples 中 7 個 Huang et al. 例子的標示與歸類都沒有問題。x=3／x=4 的處理也正確。保留語氣（may、can、potentially、likely）大致都有保留。以下列出的是真正與原文不符的地方。

## R1 問題
| 頁面 | 句子 | 原文怎麼說 | 建議修改 |
|---|---|---|---|
| definition.md（名詞釐清下方「注意」段） | 「Huang et al. 則把『faithfulness hallucination』當成幻覺的一個類別，指不忠於使用者指令或上下文的幻覺」 | 第 1 節：「faithfulness hallucination captures the divergence of generated content from user input **or the lack of self-consistency within the generated content**」，並分成 instruction、context、**logical** inconsistency 三個子類型（2.3.2 節同）。原句漏掉「內容本身不一致／邏輯矛盾」，把類別的範圍縮小了，也和 taxonomy.md 的寫法不一致 | 改為「指輸出偏離使用者的指令或上下文，或內容本身邏輯矛盾的幻覺」 |
| causes.md（「不同來源的說法」第 3 點） | 「OpenAI 認為是評估方式只看準確率、獎勵猜測；Huang et al. 則指出微調階段的傳統做法逼模型每題都答完……兩者講的是不同階段。」 | 前兩句沒問題。但「兩者講的是不同階段」是撰寫者自己加的判斷，兩份原文都沒有這樣說。而且 OpenAI 寫的是「理想上，預訓練之後的後續階段應該可以移除這些幻覺，但因為前一章節所述的理由（評估誘因），目前還無法完全做到」，也就是說 OpenAI 的評估誘因論點談的正是預訓練之後的階段，而 SFT 也屬於這個階段。說兩者在講「不同階段」，原文不支持 | 刪掉最後一句；或改成中性描述，例如「兩者的著眼點不同：OpenAI 談評估的計分方式，Huang et al. 談 SFT 的訓練做法」 |

## R2 問題
| 頁面 | 句子 | 原文怎麼說 | 建議修改 |
|---|---|---|---|
| mitigation.md（「不同來源的說法」RAG 那一點） | 「RAG 有三個來源提到：IBM 把它列為減少幻覺的方法；Ji et al. 也這樣看，但另外指出 RAG 本身的挑戰；Huang et al. 用一整節說明使用 RAG 的 LLM 仍可能產生幻覺。」 | Huang et al. 也把 RAG 列為減少幻覺的方法（5.1 節，資料相關方法的第 3 類；5.1.3：RAG「can effectively alleviate the hallucination caused by the knowledge gap」），並在第 6 節開頭稱它為「a promising strategy to mitigate hallucinations」。本頁的 Huang et al. 方法表也這樣寫。比較句只留下 Huang et al. 的「RAG 仍會幻覺」，和 IBM、Ji et al. 形成對比，結果把 Huang et al. 的立場寫偏了 | 改為「Huang et al. 也把 RAG 列為減少幻覺的方法，稱它是有希望的策略，但另用一整節說明使用 RAG 的 LLM 仍可能產生幻覺（檢索失敗、生成瓶頸）」 |

## R3 提醒
1. causes.md「過度自信」這一列只寫了注意力集中在附近的字、會忘記指令，沒有寫原文對 over-confidence 本身的說明（3.3.2）：「stems from an excessive focus on the partially generated content, often prioritizing fluency at the expense of faithfully adhering to the source context」。少了這句，學生可能會把這裡的「過度自信」誤會成 7.2 節那種「自信地說出錯誤內容」。建議補一句「過度注重已生成的內容，常為了流暢而犧牲對來源的忠實」。
2. 第 3 節的表 2、表 3 例子在收錄範圍內，但沒有收進 examples.md，對大學生很好懂：
   - imitative falsehood：訓練資料常把燈泡歸功於愛迪生，模型就答「愛迪生發明燈泡」。
   - societal bias：摘要時看到「Dr. Kim」就自行加上「來自南韓」。
   - long-tail knowledge：苯酮尿症的成因答錯，正確是 PAH 基因。
   - up-to-date knowledge：2024 年美國民主黨候選人，模型答 Michelle Obama。
   - copyright-sensitive knowledge：捏造受版權保護的小說結局。
3. 3.1.2 提到，LLM 遇到醫療、法律這類需要專業知識的問題時，「may exhibit pronounced hallucinations, often manifesting as factual fabrication」。這點和實際使用風險有關，causes.md 的知識邊界列可以補上。
4. taxonomy.md「不照指令」：原文 2.3.2 特別說明，有些偏離指令是為了遵守安全規範，這裡指的是對非惡意指令「unintentional misalignment」。不寫這句，讀者可能會把安全性拒答也當成幻覺。
5. taxonomy.md：原文把事實矛盾再細分為 entity-error 與 relation-error（愛迪生例子中，電話屬前者、燈泡屬後者），事實捏造細分為 unverifiability 與 overclaim（巴黎虎屬前者、綠建築運動屬後者）。目前只在說明欄隱約帶到，可以考慮明列。
6. mitigation.md RAG 小節：6.2 概述指出，生成瓶頸和兩種能力有關，分別是 contextual awareness 與 contextual alignment（來源歸屬、忠實解碼）。Wiki 只寫了前者包含的三個因素（雜訊、資料衝突、利用不足）。
7. causes.md 知識邊界（7.2）：原文另外提到，研究發現 LLM 內部可能有「這題無法回答」的表徵，但面對這類問題仍會過度自信而產生幻覺；能不能可靠探測 LLM 的內部信念，仍是有待研究的問題。
8. taxonomy.md 並列比較：Huang et al. 2.3 節對 extrinsic 的描述是「cannot be verified using the provided source context **or external knowledge bases**」，並稱它「potentially misleading」，和 Ji et al.「extrinsic 不一定是錯的」的說法角度不同。如果要比較兩者，這點值得一提（目前 Wiki 沒有寫錯，只是沒提）。

附註（不屬於本次 Huang et al. 審查範圍，供參考）：mitigation.md「不同來源的說法」中，前一點已經寫了 Ji et al. 也談到「允許說不知道」，後一點卻寫「『允許說不知道』三個來源都提到：IBM、OpenAI、Anthropic」，兩點的來源數不一致。
