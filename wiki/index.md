# index.md

每頁一行：`- [[slug]] — 一行摘要`。每次 ingest 後更新。

## 總覽
- [[overview]] — 一頁講完 LLM 幻覺的定義、分類、成因、例子、影響、偵測與減少方法

## 概念
- [[definition]] — 幻覺的定義（IBM、OpenAI、Anthropic）、名詞釐清（faithfulness／factuality）、定義基準與能不能避免（各來源並列）、幻覺和一般錯誤的差別
- [[taxonomy]] — 各來源的幻覺分類並列：IBM 的事實型／脈絡型／一致性型、Ji et al. 的 intrinsic／extrinsic
- [[causes]] — 幻覺的成因（IBM 的模式預測與其他成因；OpenAI 的評估誘因與預訓練；Ji et al. 的資料與訓練生成成因）
- [[impact]] — 幻覺的現實後果（醫療、假訊息、隱私），以及多 agent 流程中的連鎖幻覺
- [[detection]] — 偵測幻覺的方法：自動比對、gold-label 測試集；SimpleQA 的答對／答錯／棄答數據；Best-of-N；Ji et al. 的傳統指標限制、LLM 的兩類偵測方法（TruthfulQA）
- [[mitigation]] — 減少幻覺的方法：IBM 的企業做法；OpenAI 的改變評分方式、允許放棄不答；Anthropic 的 prompt 技巧；Ji et al. 的研究方法類別
- [[myths]] — OpenAI 提出的五個關於幻覺的迷思與研究結果

## 例子
- [[examples]] — 各來源提到的幻覺實例（判例、披薩膠水、居禮夫人、多 agent 誤刪備份、作者博士論文、猜生日）、伊波拉疫苗、TruthfulQA、吐出個人資料，以及 Anthropic 的三個 prompt 範例

## 來源摘要
- [[sources/ibm]] — IBM 的入門文章：定義、成因、三種類型、影響與企業的減少方法
- [[sources/openai]] — OpenAI 研究部落格：評估方式獎勵猜測、預訓練的來源、迷思
- [[sources/anthropic]] — Anthropic 開發者指南：允許說不知道、先摘錄原文、用引用驗證等技巧
- [[sources/ji2023]] — Ji et al. 綜述論文：NLG 幻覺的定義、intrinsic／extrinsic、成因、衡量與 LLM 的幻覺
