# 來源摘要：Anthropic〈Reduce hallucinations〉

- 出處：Claude Platform Docs（Best practices → Strengthen guardrails），使用者於 2026-11-23 存下的版本
- 類型：給開發者的官方使用指南，對象是使用 Claude 的應用程式
- 取用範圍：全文。

## 這篇講了什麼

1. **定義**：即使是最先進的語言模型（例如 Claude），有時也可能產生與事實不符，或與提供的上下文不一致的文字，這種現象稱為「hallucination」，可能損害 AI 應用的可靠性。→ [[definition]]
2. **基本技巧**：允許 Claude 說「我不知道」；長文件（超過 20k tokens）先逐字摘錄原文再作答；要求每個主張附上引用，並在寫完後逐條找支持的引文，找不到就撤回。每個技巧都附一個 prompt 範例。→ [[mitigation]]、[[examples]]
3. **進階技巧**：chain-of-thought verification、Best-of-N verification、iterative refinement、external knowledge restriction。→ [[mitigation]]、[[detection]]
4. **限制**：這些技巧能大幅減少幻覺，但無法完全消除；關鍵資訊一定要驗證，特別是高風險決策。→ [[definition]]

## 來源
- raw/anthropic.pdf
