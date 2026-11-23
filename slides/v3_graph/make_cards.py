#!/usr/bin/env python3
"""產生 slides/v3_graph/cards.json（證據卡）。quote 必須是 wiki 頁面的逐字摘錄；plain 是給大學生的白話說法。"""
import json
from pathlib import Path

C = []


def card(cid, page, source, kind, quote, plain):
    C.append({"id": cid, "page": page, "source": source, "kind": kind, "quote": quote, "plain": plain})


# ── 定義 ──
card("d01", "definition", "IBM", "fact",
     "AI 幻覺是 AI 系統產生聽起來合理、但事實錯誤、不相關或完全捏造的輸出",
     "IBM：AI 產生聽起來合理、但事實錯誤、不相關或完全捏造的輸出")
card("d02", "definition", "OpenAI", "fact",
     "幻覺是指模型自信地產生不實答案的情況",
     "OpenAI：模型自信地產生不實答案")
card("d03", "definition", "Anthropic", "fact",
     "有時也可能產生與事實不符，或與提供的上下文不一致的文字",
     "Anthropic：產生與事實不符，或與提供的上下文不一致的文字")
card("d04", "definition", "IBM", "fact",
     "會把假的事實、虛構的研究、不存在的網址，或關於真實人物與事物的錯誤細節，當成事實講出來",
     "把假的事實、虛構的研究、不存在的網址當成事實講出來")
card("d05", "definition", "IBM", "fact",
     "可能比較難發現，因為內容符合真實的模式，看起來很權威",
     "幻覺可能比較難發現：內容符合真實的模式，看起來很權威")
card("d06", "definition", "IBM", "fact",
     "IBM 把 AI 的「錯誤」（mistakes）當成較大的類別，幻覺是其中一種：系統很有自信地產生錯誤或捏造的資訊",
     "IBM：幻覺是「錯誤」的一種，系統很有自信地產生錯誤或捏造的資訊")
card("d07", "definition", "IBM", "fact",
     "通常追得到原因，可以靠補充資訊或改善訓練資料修正",
     "一般錯誤通常追得到原因，可以補充資訊或改善訓練資料修正")
card("d08", "definition", "IBM", "fact",
     "圖片標錯、提供過時的資訊、帶有偏見的建議、太籠統的回答、細微的邏輯錯誤",
     "一般錯誤的例子：圖片標錯、過時資訊、太籠統的回答")
card("d09", "definition", "IBM", "fact",
     "通常是捏造出沒有資料根據的內容",
     "幻覺通常是捏造出沒有資料根據的內容")
card("d10", "definition", "IBM", "opinion",
     "IBM 也指出，幻覺在很多方面是生成式 AI 本身就有的特性：可以減少，但無法完全消除",
     "IBM：幻覺在很多方面是生成式 AI 本身的特性，可以減少，但無法完全消除")
card("d11", "definition", "Anthropic", "opinion",
     "它介紹的減少技巧能大幅減少幻覺，但無法完全消除；關鍵資訊一定要驗證，特別是高風險決策",
     "Anthropic：它的技巧能大幅減少幻覺，但無法完全消除；關鍵資訊一定要驗證")
card("d12", "definition", "Ji et al.", "fact",
     "LLM 的回答非常流暢、有說服力，它們的幻覺更難辨識，也更可能造成傷害",
     "Ji et al.：LLM 的回答流暢、有說服力，幻覺更難辨識")

# ── 真實例子 ──
card("e01", "examples", "IBM", "example-real",
     "2023 年，一位美國律師用 ChatGPT 協助撰寫訴狀，請它提供支持論點的判例",
     "2023 年，美國律師用 ChatGPT 找支持論點的判例")
card("e02", "examples", "IBM", "example-real",
     "法院和對方律師查證後，發現其中好幾件根本不存在",
     "查證後發現好幾件判例根本不存在")
card("e03", "examples", "IBM", "example-real",
     "Google 的 AI Overview 曾建議使用者在披薩醬裡加無毒膠水，讓起司更黏；這個答案來自 2013 年 Reddit 上的一則玩笑",
     "Google AI Overview 建議在披薩醬裡加無毒膠水，答案來自 2013 年 Reddit 的玩笑")
card("e04", "examples", "OpenAI", "example-real",
     "論文作者 Adam Tauman Kalai 的博士論文是什麼題目？它信心滿滿地給了三個不同答案，沒一個正確",
     "OpenAI 問聊天機器人作者的博士論文題目，它信心滿滿給了三個不同答案，沒一個正確")
card("e05", "examples", "IBM", "example-real",
     "ChatGPT 列出一串看似權威的判例，有案名、案號和引文，格式也跟真的一樣",
     "ChatGPT 列出的判例有案名、案號和引文，格式跟真的一樣")

# ── 分類 ──
card("t01", "taxonomy", "IBM", "fact",
     "AI 說出客觀上違反真實世界的資訊，例如捏造事件、人物、統計數字或技術細節",
     "事實型：說出違反真實世界的資訊")
card("t02", "taxonomy", "IBM", "fact",
     "AI 本該依據指定的資料（例如文件或資料庫）回答，卻改用一般訓練資料",
     "脈絡型：沒照指定的資料回答")
card("t03", "taxonomy", "IBM", "fact",
     "同一段對話中前後矛盾",
     "一致性型：同一段對話前後矛盾")
card("t04", "taxonomy", "Ji et al.", "fact",
     "Intrinsic hallucination（內在幻覺） | 輸出與來源內容矛盾",
     "Intrinsic：輸出和來源矛盾")
card("t05", "taxonomy", "Ji et al.", "fact",
     "輸出無法從來源驗證，既無法被來源支持，也無法被來源否定",
     "Extrinsic：輸出無法從來源驗證")
card("t06", "taxonomy", "Huang et al.", "fact",
     "Factuality hallucination（事實幻覺）：輸出與可查證的真實世界事實不符",
     "Factuality：和真實世界事實不符")
card("t07", "taxonomy", "Huang et al.", "fact",
     "Faithfulness hallucination（忠實度幻覺）：輸出偏離使用者的輸入，或內容本身不一致",
     "Faithfulness：偏離使用者的輸入，或內容本身不一致")
card("t08", "taxonomy", "Huang et al.", "fact",
     "Huang et al. 明確表示，它的分類是在 Ji et al. 的基礎上，為 LLM 重新設計的",
     "Huang et al. 的分類是在 Ji et al. 的基礎上為 LLM 重新設計的")
card("t09", "taxonomy", "—", "fact",
     "不同來源用不同方式分類幻覺",
     "不同來源用不同方式分類幻覺")

# ── 示範例子（論文表格）──
card("x01", "examples", "Huang et al.", "example-demo",
     "問愛迪生的主要貢獻，回答「愛迪生發明了第一支實用的電話和電燈泡」",
     "問愛迪生的貢獻，答「愛迪生發明了第一支實用的電話和電燈泡」")
card("x02", "taxonomy", "Huang et al.", "example-demo",
     "實際上電話是貝爾發明的，愛迪生是改良了前人的燈泡設計",
     "實際：電話是貝爾發明的，愛迪生是改良前人的燈泡設計")
card("x03", "examples", "Huang et al.", "example-demo",
     "問艾菲爾鐵塔對環境的影響，回答「建造鐵塔導致巴黎虎滅絕，也開啟了全球綠建築運動」；巴黎虎並不存在",
     "問艾菲爾鐵塔對環境的影響，答「建造鐵塔導致巴黎虎滅絕」；巴黎虎並不存在")
card("x04", "examples", "Huang et al.", "example-demo",
     "要求把「法國的首都是什麼？」翻成西班牙文，模型卻回答「法國的首都是巴黎」",
     "要它把「法國的首都是什麼？」翻成西班牙文，它卻回答「法國的首都是巴黎」")
card("x05", "examples", "Huang et al.", "example-demo",
     "解 2x + 3 = 11，先正確得到 2x = 8，下一步卻寫 x = 3（正確為 x = 4）",
     "解 2x + 3 = 11，先得到 2x = 8，下一步卻寫 x = 3（正確為 x = 4）")
card("x06", "taxonomy", "Huang et al.", "fact",
     "事實矛盾（factual contradiction）",
     "事實矛盾")
card("x07", "taxonomy", "Huang et al.", "fact",
     "事實捏造（factual fabrication）",
     "事實捏造")
card("x08", "taxonomy", "Huang et al.", "fact",
     "不照指令（instruction inconsistency）",
     "不照指令")
card("x09", "taxonomy", "Huang et al.", "fact",
     "邏輯矛盾（logical inconsistency）",
     "邏輯矛盾")

# ── 成因 ──
card("c01", "causes", "IBM", "opinion",
     "生成式 AI 並不「知道」什麼是真、什麼是假，它只「知道」什麼符合模式",
     "IBM：AI 不「知道」真假，只「知道」什麼符合模式")
card("c02", "causes", "IBM", "opinion",
     "生成式 AI 會根據前文估計下一個 token（字或符號）是什麼",
     "根據前文，估計下一個 token（字或符號）是什麼")
card("c03", "causes", "IBM", "opinion",
     "模型追求的是在模式中顯得合理，而不是對真實世界正確",
     "追求「在模式中顯得合理」，而不是「對真實世界正確」")
card("c04", "causes", "IBM", "opinion",
     "資訊稀少或模糊時，模型就可能依過去看過的模式編造細節",
     "資訊稀少或模糊時，可能依看過的模式編造細節")
card("c05", "causes", "OpenAI", "opinion",
     "語言模型之所以會出現幻覺，是因為標準的訓練和評估流程會獎勵猜測行為，而不是承認不確定答案",
     "OpenAI：訓練和評估流程獎勵猜測，而不是承認不確定")
card("c06", "causes", "OpenAI", "example-hypo",
     "不知道答案時亂猜，也可能幸運猜對；空著不答一定零分",
     "選擇題：亂猜可能幸運猜對，空著不答一定零分")
card("c07", "causes", "OpenAI", "example-hypo",
     "模型不知道某人的生日，猜「9 月 10 日」有 1/365 的機會猜對，說「不知道」則保證零分",
     "不知道生日時猜「9 月 10 日」有 1/365 的機會猜對，說「不知道」保證零分")
card("c08", "causes", "OpenAI", "opinion",
     "測試題有幾千題時，會猜的模型在成績表上會比謹慎、不會就說不會的模型表現更好",
     "題目有幾千題時，會猜的模型成績表比謹慎的模型好看")
card("c09", "causes", "OpenAI", "opinion",
     "評估本身並不會直接導致幻覺，但大部分評估在測量模型表現時，會鼓勵猜測，而不是誠實面對不確定",
     "評估本身不會直接導致幻覺，但大部分評估會鼓勵猜測")
card("c10", "causes", "Huang et al.", "opinion",
     "遇到超出知識邊界的問題時，模型更容易產生幻覺",
     "Huang et al.：遇到超出知識邊界的問題時，模型更容易幻覺")
card("c11", "causes", "Huang et al.", "opinion",
     "模型記不住所有知識，尤其是少見的冷門知識；預訓練資料本身也不包含快速變化的新知識，以及受版權限制的內容",
     "模型記不住所有知識，尤其是冷門知識；訓練資料也不含快速變化的新知識")
card("c12", "causes", "Huang et al.", "opinion",
     "傳統 SFT 通常逼模型把每個回答都完成，不讓它表達不確定",
     "傳統的微調（SFT）通常逼模型把每個回答都完成，不讓它表達不確定")
card("c13", "causes", "Huang et al.", "opinion",
     "經過人類回饋訓練的模型，有時會為了討好評估者而犧牲正確性，稱為 sycophancy（諂媚）",
     "經過人類回饋訓練的模型，有時會為了討好評估者而犧牲正確性（sycophancy，諂媚）")
card("c14", "causes", "Ji et al.", "opinion",
     "有研究發現模型會優先使用這些知識，而不是輸入的資料",
     "Ji et al. 引用研究：模型會優先用自己記住的知識，而不是輸入的資料")
card("c15", "causes", "IBM", "opinion",
     "模型完全從看過的資料學習。資料若有事實錯誤、偏見或缺漏，模型會把它們當成正常的模式學起來",
     "IBM：訓練資料若有錯誤、偏見或缺漏，模型會當成正常的模式學起來")
card("c16", "causes", "OpenAI", "opinion",
     "像寵物生日這種任意的低頻率事實，不能單從模式預測，因而會導致幻覺",
     "OpenAI：像寵物生日這種任意的冷門事實，無法單從模式預測")

# ── 數據（SimpleQA）──
card("n01", "detection", "OpenAI", "fact",
     "棄答率（不提供具體答案） | 52% | 1%",
     "棄答率（不提供具體答案）：gpt-5-thinking-mini 52%，o4-mini 1%")
card("n02", "detection", "OpenAI", "fact",
     "準確率（越高越好） | 22% | 24%",
     "準確率：gpt-5-thinking-mini 22%，o4-mini 24%")
card("n03", "detection", "OpenAI", "fact",
     "錯誤率（越低越好） | 26% | 75%",
     "錯誤率：gpt-5-thinking-mini 26%，o4-mini 75%")
card("n04", "detection", "OpenAI", "opinion",
     "o4-mini 的準確率稍微超前，但錯誤率（也就是幻覺率）明顯較高",
     "o4-mini 準確率稍高，但錯誤率（幻覺率）明顯較高")
card("n05", "detection", "OpenAI", "opinion",
     "多數成績表以準確率優先，但答錯比放棄不答更糟",
     "OpenAI：答錯比放棄不答更糟")
card("n06", "detection", "OpenAI", "fact",
     "OpenAI 引用 GPT‑5 系統說明卡中的 SimpleQA 評估",
     "數據出自 OpenAI 引用的 SimpleQA 評估")

# ── 影響 ──
card("i01", "impact", "IBM", "opinion",
     "醫療 AI 可能產生偽陽性，例如把良性的皮膚病灶判斷為惡性，導致不必要的醫療處置",
     "醫療：可能把良性的皮膚病灶判斷為惡性")
card("i02", "impact", "IBM", "opinion",
     "如果新聞機器人在緊急事件發生時，回答了未經查證的資訊，可能迅速散布錯誤訊息",
     "假訊息：緊急事件時回答未經查證的資訊，可能迅速散布錯誤訊息")
card("i03", "impact", "Ji et al.", "opinion",
     "語言模型可能被誘導還原並產生訓練資料中的個人敏感資訊（例如 email、電話、地址）",
     "隱私：可能被誘導產生訓練資料中的 email、電話、地址")
card("i04", "impact", "IBM", "opinion",
     "在多個 agent 或多個步驟串接的流程中，一個幻覺可能成為後續步驟的前提",
     "IBM：多個 agent 或多個步驟串接時，一個幻覺可能成為後續步驟的前提")
card("i05", "impact", "IBM", "example-hypo",
     "Agent A 捏造一個錯誤 → Agent B 依據這個錯誤檢索或推理 → Agent C 摘要 B 的輸出 → 最後產出一個包裝完整、看似前後一致，但前提是錯的答案",
     "A 捏造錯誤 → B 依據它推理 → C 摘要 → 包裝完整、但前提是錯的答案")
card("i06", "examples", "IBM", "example-hypo",
     "結果那是公司唯一一份仍受法律保存要求的財務交易紀錄",
     "IBM 的假設情境：被刪掉的是公司唯一一份須依法保存的財務紀錄")
card("i07", "impact", "Ji et al.", "opinion",
     "機器翻譯的藥物說明若有幻覺，可能引發危及生命的事件",
     "醫療：翻譯藥物說明時出現幻覺，可能危及生命")

# ── 偵測 ──
card("v01", "detection", "IBM", "fact",
     "自動幻覺偵測系統會把模型輸出和參考來源比對，檢查每個主張是否有證據支持",
     "IBM：把輸出和參考來源比對，檢查每個主張有沒有證據")
card("v02", "detection", "Anthropic", "fact",
     "用同一個 prompt 讓 Claude 跑多次並比較輸出，輸出之間不一致可能代表有幻覺",
     "Anthropic：同一題問多次，答案不一致可能代表有幻覺")
card("v03", "detection", "Ji et al.", "fact",
     "同一個問題生成多次，看答案是否一致",
     "Ji et al.：同一個問題生成多次，看答案是否一致")
card("v04", "detection", "IBM", "fact",
     "gold-label 測試集是一組精選的輸入，每題都有經過驗證的權威答案",
     "IBM：用每題都有權威答案的測試集（gold-label）定期評估")
card("v05", "detection", "Huang et al.", "fact",
     "先把回答拆成一條條獨立的事實陳述，再拿可信的知識來源逐條查證",
     "Huang et al.：把回答拆成一條條事實，再拿可信來源逐條查證")
card("v06", "detection", "Ji et al.", "fact",
     "人工評估仍是最常用的方法之一",
     "Ji et al.：人工評估仍是最常用的方法之一")

# ── 減少 ──
card("m01", "mitigation", "IBM", "fact",
     "把模型接上精選的知識庫，要求它只用知識庫的內容回答",
     "RAG：接上精選的知識庫，只用知識庫的內容回答")
card("m02", "mitigation", "IBM", "fact",
     "在幻覺可能造成重大傷害的地方（例如法律意見、法規文件）安排人工審核",
     "人工審核：在可能造成重大傷害的地方（例如法律意見）安排人工審核")
card("m03", "mitigation", "IBM", "fact",
     "也常搭配「不確定就說不知道」這類防護規則",
     "Prompt 裡加上「不確定就說不知道」這類規則")
card("m04", "mitigation", "OpenAI", "opinion",
     "模型自信地答錯時，扣得比表達不確定時更多；模型適當表達不確定時，給予部分分數",
     "改評分：自信答錯扣得比表達不確定更多，表達不確定給部分分數")
card("m05", "mitigation", "OpenAI", "opinion",
     "表達不確定或要求釐清問題，比自信地提供錯誤資訊來得好",
     "OpenAI 的模型規格：表達不確定或要求釐清，比自信答錯好")
card("m06", "mitigation", "Anthropic", "fact",
     "明確允許 Claude 承認不確定。Anthropic 表示，這個技巧可以大幅減少錯誤資訊",
     "允許說「我不知道」：Anthropic 表示可以大幅減少錯誤資訊")
card("m07", "mitigation", "Anthropic", "fact",
     "要求 Claude 為每個主張附上引文與來源，讓回答可以被檢查",
     "要求每個主張附上引文與來源")
card("m08", "mitigation", "Anthropic", "fact",
     "明確指示 Claude 只能使用提供的文件，不能用它的一般知識",
     "只准用提供的文件，不能用一般知識")
card("m09", "mitigation", "Huang et al.", "opinion",
     "使用 RAG 的 LLM 仍可能產生幻覺",
     "Huang et al.：使用 RAG 的 LLM 仍可能產生幻覺")
card("m10", "mitigation", "Huang et al.", "opinion",
     "檢索失敗：使用者的問題寫得不清楚或模糊、檢索的資料來源不可靠或範圍不足、檢索器本身效果不好",
     "原因之一：檢索失敗，例如問題模糊、資料來源不可靠")

card("m11", "mitigation", "—", "fact",
     "IBM 的方法多從企業與開發者的角度出發（訓練資料、fine-tune、RAG、prompt、人工審核、治理）；OpenAI 則把重點放在模型的訓練與評估方式；Anthropic 列出的是使用 Claude 時的技巧",
     "IBM 從企業與開發者角度；OpenAI 著重訓練與評估方式；Anthropic 是使用 Claude 時的技巧")

# ── 能不能避免 ──
card("a01", "myths", "OpenAI", "opinion",
     "幻覺不可避免 | 並非如此，因為語言模型可在不確定答案時放棄不答",
     "OpenAI：「幻覺不可避免」是迷思，因為模型可在不確定時放棄不答")
card("a02", "overview", "Anthropic", "fact",
     "Anthropic 沒有討論幻覺本質上能不能避免",
     "Anthropic 沒有討論幻覺本質上能不能避免")
card("a03", "myths", "OpenAI", "opinion",
     "準確率絕不會達到 100%，因為不論模型的規模、搜尋和推理功能如何，現實世界中有些問題就是沒有答案",
     "OpenAI：準確率絕不會達到 100%，因為有些問題就是沒有答案")

Path(__file__).with_name("cards.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(C), "cards")
