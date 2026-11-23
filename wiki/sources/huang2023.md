# 來源摘要：Huang et al.〈A Survey on Hallucination in Large Language Models〉

- 作者：Lei Huang 等人（哈爾濱工業大學、華為）
- 發表：ACM Transactions on Information Systems；使用者下載的是 arXiv v2（2024-11-19）
- 類型：學術綜述論文，專門討論 LLM 的幻覺
- 取用範圍：第 1–2 節（引言、定義、分類）、第 3 節（成因）、第 4.1 節（偵測方法的分類）、第 5 節開頭（減少方法的分類）、第 6 節開頭（RAG 也會幻覺）、第 7.2 節（知識邊界）。benchmark 清單與各方法的技術細節不收錄（ingest 討論時決定，以好懂為主）。
- 原文註記：第 2.3 節「邏輯矛盾」的例子，表 1 寫模型錯答 x=3，內文寫 x=4。驗算 2x+3=11 的正確答案是 x=4，表 1 的說明也寫「把 8 除以 2 算成 3」，因此內文的 x=4 應為筆誤；Wiki 採用表 1 的版本。

## 這篇講了什麼

1. **定義**：LLM 容易產生幻覺，也就是看似合理但不符合事實的內容；LLM 的幻覺範圍更廣，主要表現為事實錯誤。→ [[definition]]
2. **分類**：建立在 Ji et al. 的基礎上，重新為 LLM 設計：factuality 與 faithfulness 兩大類、共 5 個子類型。→ [[taxonomy]]
3. **成因**：資料、訓練、生成（inference）三方面。→ [[causes]]
4. **偵測**：factuality 幻覺的偵測（查證事實、估計不確定性）與 faithfulness 幻覺的偵測。→ [[detection]]
5. **減少方法**：依成因分成資料相關、訓練相關、生成相關三類。→ [[mitigation]]
6. **RAG 也會幻覺**：檢索失敗與生成瓶頸。→ [[mitigation]]
7. **知識邊界**：LLM 不太能辨認自己知識的邊界，因而自信地說出錯誤內容。→ [[causes]]

## 來源
- raw/huang2023.pdf
