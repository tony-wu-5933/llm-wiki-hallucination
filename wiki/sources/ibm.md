# 來源摘要：IBM〈What are AI hallucinations?〉

- 作者：Chrystal R. China（IBM Think）
- 發布：2023-09-01，更新：2026-07-31
- 類型：企業的入門介紹文章
- 取用範圍：全文的說明段落。文末的 IBM 產品介紹、調查數據與推廣內容不收錄（ingest 討論時決定）。

## 這篇講了什麼

1. **定義與範圍**：AI 幻覺是 AI 系統產生聽起來合理、但事實錯誤、不相關或完全捏造的輸出，例如假的事實、虛構的研究、不存在的網址、關於真實對象的錯誤細節。幻覺在很多方面是生成式 AI 本身就有的特性，可以減少，但無法完全消除。影像、聲音、影片生成模型也可能產生 confabulation。→ [[definition]]
2. **幻覺和一般錯誤的差別**：一般錯誤通常是某個細節或假設錯了，原因追得到；幻覺通常是沒有資料根據的捏造內容，因為符合真實的模式而顯得權威，所以可能更難發現。→ [[definition]]
3. **成因**：模型依訓練資料的模式預測「下一個 token」，追求的是合理，而不是對世界正確；其他成因包括訓練資料有缺陷或不足、設計本身的限制、overfitting 與虛假的關聯、對抗式輸入（例如 prompt injection）。→ [[causes]]
4. **三種類型**：core factual、contextual、consistency。→ [[taxonomy]]
5. **例子**：律師引用 ChatGPT 捏造的判例、Google AI Overview 建議在披薩醬裡加膠水、居禮夫人得獎資訊被講錯、多 agent 流程中的連鎖幻覺。→ [[examples]]
6. **影響**：醫療誤判、假訊息擴散、多 agent 流程中的 cascading hallucination。→ [[impact]]
7. **減少方法**：高品質訓練資料、慎選與 fine-tune 模型、RAG、prompt engineering、human in the loop、AI governance。→ [[mitigation]]
8. **偵測與監控**：自動比對輸出與參考資料、benchmark 與 gold-label 測試集。→ [[detection]]

## 來源
- raw/ibm.pdf
