# 審查報告：ingest 1（IBM）第 2 輪
- 結論：不通過（只剩 2 處小問題，都是 R2，改完即可通過）

## 上一輪問題的修正狀態
| 問題 | 狀態 |
|---|---|
| R1：examples.md 律師案例的類型欄填「事實型」 | 已修正（改為「原文未歸類，用來說明成因」） |
| R1：examples.md 多 agent 案例未標明是假設情境（居禮夫人、藥物兩列同理） | 已修正（新增「真實事件／假設情境」欄：律師、披薩為真實事件，居禮夫人為示範句，藥物、多 agent 為假設情境） |
| R1：impact.md「前提是錯的完美答案」 | 已修正（改為「包裝完整、看似前後一致」） |
| R2：overview.md 第 1 點未標明 IBM 定義、「所以更難發現」 | 已修正（加「依 IBM 的定義」，改「可能更難發現」） |
| R2：overview.md 第 7 點「只能減少，無法完全消除」未標明 IBM、去掉 in many ways | 已修正 |
| R2：overview.md 第 5 點「會被當成事實一路放大」 | 已修正（改「可能」並註明 IBM） |
| R2：impact.md「會放大幻覺的影響」 | 已修正（改「可能放大」） |
| R2：impact.md 連鎖幻覺未保留 often | 已修正（改「結果常常形成連鎖幻覺」） |
| R2：definition.md 表格「比較難發現」「捏造出完全沒有資料根據」「真實的語言模式」 | 已修正（改為「可能比較難發現」「通常是捏造出沒有資料根據的內容」「真實的模式」） |
| R2：sources/ibm.md 第 2 點缺「通常」「可能」、多了「語言」 | 已修正 |

## 新發現的 R1／R2 問題
| 頁面 | 句子 | 原文怎麼說 | 建議修改 |
|---|---|---|---|
| sources/ibm.md | 第 1 點：「幻覺是生成式 AI 本身就有的特性，可以減少，但無法完全消除。」 | "But in many ways, hallucinations are inherent to generative AI. They can be reduced but not fully eliminated." 原文有 "in many ways" 的保留。overview.md 和 definition.md 已依上一輪改成「在很多方面」，這一頁漏改（R2） | 改成「幻覺在很多方面是生成式 AI 本身就有的特性，可以減少，但無法完全消除。」 |
| mitigation.md | Prompt engineering 列：「模糊的 prompt 會讓模型去猜使用者要什麼。」 | "Poorly structured or vague prompts can trigger hallucinations, inviting the model to guess what the user is looking for." 原文是 "can"，而且重點是「可能引發幻覺」（R2，去掉保留語氣） | 改成「結構不良或模糊的 prompt 可能引發幻覺，讓模型去猜使用者要什麼。」 |

其餘頁面（definition.md、causes.md、taxonomy.md、examples.md、impact.md、detection.md、overview.md）逐句對照原文，沒有發現與原文意思不符或把 IBM 觀點寫成普遍事實的句子。
