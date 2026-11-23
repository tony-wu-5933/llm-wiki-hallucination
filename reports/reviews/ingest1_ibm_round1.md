# 審查報告：ingest 1（IBM）第 1 輪
- 結論：不通過

## R1 問題
| 頁面 | 頁面中的句子 | 原文怎麼說（引用原文短句） | 建議修改 |
|---|---|---|---|
| examples.md | 「律師引用不存在的判例」一列的「類型」欄填「事實型」 | 原文把律師案例放在 "Why do AI hallucinations occur?" 段落，用來說明 "The AI model stitched together plausible-sounding case names..."，沒有把它歸到 core factual、contextual 或 consistency 任何一類 | 類型欄改成「原文未分類」或留空。如果要保留「事實型」，要標明是 wiki 自己的推論，不是 IBM 的分類 |
| examples.md | 「多 agent 誤刪備份」：「公司用 agent 流程降低雲端儲存費用……結果那是公司唯一一份仍受法律保存要求的財務交易紀錄」（欄名「發生了什麼」） | "Say that a company runs an agentic workflow to reduce cloud storage costs." 原文是假設情境，不是真實事件 | 標明「（IBM 的假設情境）」。居禮夫人一列（原文給的是示範句）和藥物一列（原文寫 "If an AI chatbot states..."）也一樣，建議加一欄「真實事件／假設情境」。律師案例和披薩膠水案例才是原文說的真實事件（"in 2023 a US lawyer..."、"For a real-world example..."） |
| impact.md | 「最後產出一個看起來前後一致、但前提是錯的完美答案」 | "the system produces a polished answer that feels internally consistent" | 「完美」改成「包裝完整、看似精緻」。"polished" 指表面修飾得好，沒有「完美」的意思 |

## R2 問題
| 頁面 | 頁面中的句子 | 原文怎麼說（引用原文短句） | 建議修改 |
|---|---|---|---|
| overview.md | 第 1 點：「LLM 很有自信地說出聽起來合理、但其實錯誤或捏造的內容……它和一般錯誤不同，因為聽起來很對，所以更難發現。」 | 這是 IBM 的定義和區分方式（"AI hallucinations are a specific type of mistake where the system confidently generates false or fabricated information"），而且原文寫的是 "They can be harder to spot" | 開頭加上「依 IBM 的定義」；「所以更難發現」改成「所以可能更難發現」 |
| overview.md | 第 7 點：「幻覺只能減少，無法完全消除。」 | "But in many ways, hallucinations are inherent to generative AI. They can be reduced but not fully eliminated."（IBM 的觀點，而且有 "in many ways" 的保留） | 改成「IBM 認為，幻覺在很多方面是生成式 AI 本身就有的特性，只能減少，無法完全消除。」 |
| overview.md | 第 5 點：「在多 agent 流程中，一個幻覺會被當成事實一路放大。」 | "a single hallucination can become a starting assumption for later steps"；"The proliferation of autonomous AI agents can amplify the impact" | 「會」改成「可能」，並註明是 IBM 的說法 |
| impact.md | 「IBM 指出，自主 AI agent 越來越普及，會放大幻覺的影響。」 | "The proliferation of autonomous AI agents can amplify the impact of hallucinations." | 「會放大」改成「可能放大」 |
| impact.md | 「後面的 agent 不只是重複錯誤，還會在上面建立更多推理，形成連鎖幻覺（cascading hallucination）。」 | "The result is often a cascading hallucination" | 改成「結果常常形成連鎖幻覺」，保留 "often" |
| definition.md | 表格「好不好發現」列，幻覺欄：「比較難發現，因為內容符合真實的語言模式，看起來很權威」；「問題出在哪」與「例子」列的幻覺欄：「捏造出完全沒有資料根據的內容」 | "They can be harder to spot than other mistakes"；"Hallucinations generally involve AI models producing fabricated content that has no grounding in real data." 另外，原文只寫 "real patterns"，沒有寫「語言」 | 改成「可能比較難發現」「通常是捏造出沒有資料根據的內容」；「真實的語言模式」改成「真實的模式」 |
| sources/ibm.md | 第 2 點：「幻覺是沒有根據的捏造內容，因為符合真實的語言模式而顯得權威，所以更難發現。」 | 同上："generally involve..."、"can be harder to spot"、"adherence to real patterns" | 加上「通常」「可能」，刪掉「語言」 |

## R3 提醒
- 原文說幻覺不只出現在 LLM：「Image, audio and video generators ... might create confabulations」「An image generation platform might create images with inaccurate captions or nonsensical objects」。原文也用了 confabulation 這個說法。所有頁面都沒有提到，可以考慮在 definition.md 補一句範圍說明。
- causes.md 的「訓練資料有缺陷」一列沒有收錄原文的核心理由：「It can't discern which patterns are accurate reflections of the world and which ones are artifacts of noisy or problematic data.」
- causes.md 的「對抗式輸入」一列沒有收錄「Because the AI can't discern a user's intentions, it treats tricky inputs like any other text」，也沒有收錄這類輸入會讓模型 "ignore cybersecurity rules or override guardrails"。
- mitigation.md 沒有收錄「If the fine-tuning step is skipped or done with poor-quality data, the model is more likely to hallucinate.」
- mitigation.md 提到「資料範本與 chain-of-thought prompting」，但沒有寫原文對這兩者的說明（"Data templates are reusable, predefined patterns that standardize how users talk to a model"、"Chain-of-thought prompting asks the model to reason in steps"）。
- mitigation.md 的 AI governance 一列只寫了 risk tiering，沒有收錄原文的其他內容：權責分工（"define who is responsible for hallucination risk across legal, compliance, technology and business lines"），在流程中嵌入審核步驟（例如送給客戶前要有 "verified" 狀態），以及把 AI 輸出當成必須檢查的草稿、避免 "good enough" 文化。另外，Human in the loop 一列沒有寫原文說的「也會產生回饋，用來改善 prompt 和系統設定」。
- 非內容問題：每一頁的「來源」都寫 raw/ibm.pdf，但這次提供的原文是 raw/text/ibm.txt，上傳的資料夾裡沒有 raw/ibm.pdf。請確認路徑是否需要統一。
