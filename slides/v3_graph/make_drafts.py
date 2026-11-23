#!/usr/bin/env python3
"""逐頁稿節點：依 outline.md 與 cards.json 寫出 drafts/slide_XX.json。
規則：每段文字只能改寫自所引用證據卡的 quote／plain，不可加入卡片沒有的內容。"""
import json
from pathlib import Path

D = Path(__file__).with_name("drafts")
D.mkdir(exist_ok=True)


def it(text, *cards):
    return {"text": text, "cards": list(cards)}


S = {}

S[1] = {"type": "title", "title": "LLM 幻覺是什麼？",
        "subtitle": "當 AI 一本正經地說錯話：定義、例子、成因與因應（Graph 版：只用 Wiki 證據卡組成）",
        "blocks": [{"type": "icon", "name": "chat"}]}

S[2] = {"type": "content", "title": "幻覺是什麼？",
        "core": it("IBM、OpenAI、Anthropic 對幻覺各有定義，並列呈現", "d01", "d02", "d03"),
        "blocks": [
            {"type": "columns", "cols": [
                {"head": "IBM", "items": [it("AI 產生聽起來合理、但事實錯誤、不相關或完全捏造的輸出", "d01"),
                                          it("把假的事實、虛構的研究、不存在的網址當成事實講出來", "d04")]},
                {"head": "OpenAI", "items": [it("模型自信地產生不實答案", "d02")]},
                {"head": "Anthropic", "items": [it("產生與事實不符，或與提供的上下文不一致的文字", "d03")]},
            ]}]}

S[3] = {"type": "content", "title": "真的發生過的幻覺",
        "core": it("下面兩個都是真實發生過的事件（IBM 舉例）", "e01", "e03"),
        "layout": "row",
        "blocks": [
            {"type": "chat", "label": "真實事件（2023）；提問為情境重現",
             "q": it("請提供支持我論點的判例", "e01"),
             "a": {"text": "列出一串判例，有案名、案號和引文，格式跟真的一樣", "cards": ["e05"], "wrong": []},
             "note": it("查證後發現好幾件判例根本不存在", "e02")},
            {"type": "chat", "label": "真實事件；提問為情境重現",
             "q": it("想讓披薩上的起司更黏", "e03"),
             "a": {"text": "在披薩醬裡加無毒膠水", "who": "Google AI Overview", "cards": ["e03"], "wrong": ["加無毒膠水"]},
             "note": it("這個答案來自 2013 年 Reddit 的玩笑", "e03")},
        ]}

S[4] = {"type": "content", "title": "幻覺和一般錯誤",
        "core": it("IBM：幻覺是「錯誤」的一種，系統很有自信地產生錯誤或捏造的資訊", "d06"),
        "blocks": [
            {"type": "columns", "cols": [
                {"head": "一般錯誤", "items": [it("例子：圖片標錯、過時資訊、太籠統的回答", "d08"),
                                           it("通常追得到原因，可以補充資訊或改善訓練資料修正", "d07")]},
                {"head": "幻覺", "items": [it("通常是捏造出沒有資料根據的內容", "d09"),
                                         it("可能比較難發現：內容符合真實的模式，看起來很權威", "d05")]},
            ]},
            {"type": "callout", "tag": "Ji et al.", "text": "LLM 的回答流暢、有說服力，幻覺更難辨識", "cards": ["d12"]},
        ]}

S[5] = {"type": "content", "title": "幻覺有哪幾種？",
        "core": it("不同來源用不同方式分類幻覺", "t09"),
        "blocks": [
            {"type": "columns", "cols": [
                {"head": "IBM：3 種", "items": [it("事實型：說出違反真實世界的資訊", "t01"),
                                              it("脈絡型：沒照指定的資料回答", "t02"),
                                              it("一致性型：同一段對話前後矛盾", "t03")]},
                {"head": "Ji et al.：2 種", "items": [it("Intrinsic：輸出和來源矛盾", "t04"),
                                                    it("Extrinsic：輸出無法從來源驗證", "t05")]},
                {"head": "Huang et al.：2 大類", "items": [it("Factuality：和真實世界事實不符", "t06"),
                                                        it("Faithfulness：偏離使用者的輸入，或內容本身不一致", "t07"),
                                                        it("在 Ji et al. 的基礎上為 LLM 重新設計", "t08")]},
            ]}]}

S[6] = {"type": "content", "title": "Huang et al. 的示範例子",
        "core": it("以下是論文表格中的示範例子，不是真實事件", "x01", "x03"),
        "blocks": [
            {"type": "chats", "items": [
                {"label": "示範例子：事實矛盾",
                 "q": it("愛迪生的主要貢獻是什麼？", "x01"),
                 "a": {"text": "愛迪生發明了第一支實用的電話和電燈泡", "cards": ["x01", "x06"], "wrong": ["發明了第一支實用的電話和電燈泡"]},
                 "note": it("實際：電話是貝爾發明的；燈泡是愛迪生改良前人的設計", "x02")},
                {"label": "示範例子：事實捏造",
                 "q": it("艾菲爾鐵塔對環境有什麼影響？", "x03"),
                 "a": {"text": "建造鐵塔導致巴黎虎滅絕", "cards": ["x03", "x07"], "wrong": ["巴黎虎滅絕"]},
                 "note": it("實際：巴黎虎並不存在", "x03")},
                {"label": "示範例子：不照指令",
                 "q": it("把「法國的首都是什麼？」翻成西班牙文", "x04"),
                 "a": {"text": "法國的首都是巴黎", "cards": ["x04", "x08"], "wrong": ["法國的首都是巴黎"]},
                 "note": it("錯在哪：要的是翻譯，它卻直接回答問題", "x04")},
                {"label": "示範例子：邏輯矛盾",
                 "q": it("解 2x + 3 = 11", "x05"),
                 "a": {"text": "2x = 8，所以 x = 3", "cards": ["x05", "x09"], "wrong": ["x = 3"]},
                 "note": it("實際：x = 4 才正確", "x05")},
            ]},
        ]}

S[7] = {"type": "content", "title": "為什麼會發生？① 預測下一個字",
        "core": it("IBM：AI 不「知道」真假，只「知道」什麼符合模式", "c01"),
        "blocks": [
            {"type": "flow", "label": "IBM 的說法", "steps": [
                it("根據前文，估計下一個 token（字或符號）是什麼", "c02"),
                it("追求「在模式中顯得合理」，而不是「對真實世界正確」", "c03"),
                it("資訊稀少或模糊時，可能依看過的模式編造細節", "c04")]},
        ]}

S[8] = {"type": "content", "title": "為什麼會發生？② 評分方式鼓勵「猜」",
        "core": it("OpenAI：訓練和評估流程獎勵猜測，而不是承認不確定", "c05"),
        "layout": "row",
        "blocks": [
            {"type": "chat", "label": "OpenAI 的假設情境",
             "q": it("某人的生日是哪一天？", "c07"),
             "a": {"text": "9 月 10 日", "cards": ["c07"], "wrong": ["9 月 10 日"]},
             "note": it("猜有 1/365 的機會猜對，說「不知道」保證零分", "c07")},
            {"type": "bullets", "items": [
                it("像選擇題：亂猜可能幸運猜對，空著不答一定零分", "c06"),
                it("題目有幾千題時，會猜的模型成績表比謹慎的模型好看", "c08"),
                it("評估本身不會直接導致幻覺，但大部分評估會鼓勵猜測", "c09")]},
        ]}

S[9] = {"type": "content", "title": "OpenAI 引用的數據",
        "core": it("OpenAI 的解讀：o4-mini 準確率稍高，但錯誤率（也就是幻覺率）明顯較高", "n04"),
        "layout": "row",
        "blocks": [
            {"type": "bar", "title": "SimpleQA 評估（OpenAI 引用）", "unit": "%",
             "series": ["gpt-5-thinking-mini", "OpenAI o4-mini"],
             "groups": [{"name": "棄答率", "values": [52, 1]},
                        {"name": "準確率", "values": [22, 24]},
                        {"name": "錯誤率", "values": [26, 75]}],
             "cards": ["n01", "n02", "n03", "n06"]},
            {"type": "bullets", "items": [
                it("棄答率：不提供具體答案", "n01"),
                it("準確率越高越好，錯誤率越低越好", "n02", "n03"),
                it("OpenAI：答錯比放棄不答更糟", "n05")]},
        ]}

S[10] = {"type": "content", "title": "為什麼會發生？③ 其他來源的說法",
         "core": it("除了上面兩點，各來源還提出其他成因", "c15", "c14", "c10"),
         "blocks": [
             {"type": "columns", "cols": [
                 {"head": "IBM", "items": [it("訓練資料若有錯誤、偏見或缺漏，模型會當成正常的模式學起來", "c15")]},
                 {"head": "OpenAI", "items": [it("像寵物生日這種任意的冷門事實，無法單從模式預測", "c16")]},
                 {"head": "Ji et al.", "items": [it("引用研究：模型會優先用自己記住的知識，而不是輸入的資料", "c14")]},
                 {"head": "Huang et al.", "items": [it("遇到超出知識邊界的問題（例如冷門知識）時更容易幻覺", "c10", "c11"),
                                                   it("傳統的微調做法通常不讓模型表達不確定", "c12"),
                                                   it("經過人類回饋訓練的模型，有時會為了討好評估者而犧牲正確性（諂媚）", "c13")]},
             ]}]}

S[11] = {"type": "content", "title": "為什麼要在意？",
         "core": it("IBM：多個 agent 或多個步驟串接時，一個幻覺可能成為後續步驟的前提", "i04"),
         "blocks": [
             {"type": "flow", "label": "IBM 描述的連鎖幻覺", "steps": [
                 it("Agent A 捏造一個錯誤", "i05"),
                 it("Agent B 依據這個錯誤檢索或推理", "i05"),
                 it("Agent C 摘要 B 的輸出", "i05"),
                 it("包裝完整、但前提是錯的答案", "i05")]},
             {"type": "columns", "cols": [
                 {"head": "IBM 舉出的影響", "items": [
                     it("醫療 AI 可能把良性的皮膚病灶判斷為惡性", "i01"),
                     it("新聞機器人若在緊急事件時回答未經查證的資訊，可能迅速散布錯誤訊息", "i02")]},
                 {"head": "Ji et al. 舉出的影響", "items": [
                     it("翻譯藥物說明時出現幻覺，可能危及生命", "i07"),
                     it("引用研究：語言模型可能被誘導產生訓練資料中的個人資料（email、電話、地址）", "i03")]},
             ]},
         ]}

S[12] = {"type": "content", "title": "怎麼發現幻覺？",
         "core": it("把輸出和可信來源比對，或同一題問多次看答案是否一致", "v01", "v02"),
         "blocks": [
             {"type": "columns", "cols": [
                 {"head": "和來源比對", "items": [it("IBM：把輸出和參考來源比對，檢查每個主張有沒有證據", "v01"),
                                             it("Huang et al.：把回答拆成一條條事實，再拿可信來源逐條查證", "v05")]},
                 {"head": "問很多次", "items": [it("Anthropic：同一題問多次，答案不一致可能代表有幻覺", "v02"),
                                            it("Ji et al.：同一個問題生成多次，看答案是否一致", "v03")]},
                 {"head": "測試與人工", "items": [it("IBM：用每題都有權威答案的測試集（gold-label）定期評估", "v04"),
                                             it("Ji et al.：人工評估仍是最常用的方法之一", "v06")]},
             ]}]}

S[13] = {"type": "content", "title": "怎麼減少幻覺？",
         "core": it("IBM 從企業與開發者角度；OpenAI 著重訓練與評估方式；Anthropic 是使用 Claude 時的技巧", "m11"),
         "blocks": [
             {"type": "columns", "cols": [
                 {"head": "IBM", "items": [it("RAG：接上精選的知識庫，只用知識庫的內容回答", "m01"),
                                          it("在可能造成重大傷害的地方（例如法律意見）安排人工審核", "m02"),
                                          it("Prompt 裡加上「不確定就說不知道」這類規則", "m03")]},
                 {"head": "OpenAI", "items": [it("改評分：自信答錯扣得比表達不確定更多", "m04"),
                                             it("模型規格：表達不確定或要求釐清，比自信答錯好", "m05")]},
                 {"head": "Anthropic", "items": [it("允許說「我不知道」", "m06"),
                                                it("要求每個主張附上引文與來源", "m07"),
                                                it("只准用提供的文件，不能用一般知識", "m08")]},
             ]},
             {"type": "callout", "tag": "注意", "text": "Huang et al.：使用 RAG 的 LLM 仍可能產生幻覺，例如問題模糊、資料來源不可靠導致檢索失敗", "cards": ["m09", "m10"]},
         ]}

S[14] = {"type": "content", "title": "幻覺能不能完全避免？",
         "core": it("各來源說法不同，這裡並列，不判斷誰對", "d10", "a01"),
         "blocks": [
             {"type": "columns", "cols": [
                 {"head": "IBM", "items": [it("幻覺在很多方面是生成式 AI 本身的特性，可以減少，但無法完全消除", "d10")]},
                 {"head": "OpenAI", "items": [it("「幻覺不可避免」是迷思，因為模型可在不確定時放棄不答", "a01"),
                                             it("準確率絕不會達到 100%，因為有些問題就是沒有答案", "a03")]},
                 {"head": "Anthropic", "items": [it("沒有討論幻覺本質上能不能避免", "a02"),
                                                it("它的技巧能大幅減少幻覺，但無法完全消除；關鍵資訊一定要驗證", "d11")]},
             ]}]}

S[15] = {"type": "summary", "title": "總結",
         "blocks": [{"type": "bullets", "items": [
             it("定義：各來源不同；IBM 說是聽起來合理、但事實錯誤或捏造的輸出", "d01"),
             it("分類：不同來源用不同方式分類幻覺", "t09"),
             it("成因：IBM 說模型追求「在模式中顯得合理」；OpenAI 說訓練和評估流程獎勵猜測", "c03", "c05"),
             it("影響：IBM 指出多 agent 流程中，一個幻覺可能成為後續步驟的前提", "i04"),
             it("偵測與減少：比對來源、問多次；RAG、人工審核、允許說不知道", "v01", "v02", "m01", "m02", "m06"),
             it("能不能避免：IBM 認為只能減少；OpenAI 認為不是不可避免；Anthropic 沒有討論，只說它的技巧無法完全消除幻覺", "d10", "a01", "a02", "d11")]}]}

for k, s in S.items():
    (D / f"slide_{k:02d}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "drafts")
