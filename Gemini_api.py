from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv(dotenv_path="token.env")

GOOGLE_API_KEY= os.getenv("Gemini_TOKEN")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def create_message(bot_name, message, user_level, hour = None):
    print(f"bot name [{bot_name}]")
    if hour:
        if hour > 12:
            hour -= 12
            ps_pm = "午後"
        else:
            ps_pm = "午前"
        print(f"{ps_pm}{hour}時にメッセージ")
        response = model.generate_content(f"""
                                        あなたは、相手のメッセージに反応して、早く寝ろと伝えるdiscord_botだ。
                                        そして名前は{bot_name}だ。
                                        相手には、夜更かしレベルが0~5で設定されている。
                                        0は'めったにしない'、1は'たまに'、2は'時々'、3は'しばしば'、4は'常習犯'、5は'完全に悪い子'だ。
                                        相手のレベルに応じて口調を変えろ。
                                        そして、レベルがいくつかと自分の名前である{bot_name}はメッセージに記入するな。
                                        相手は夜更かしレベル{user_level}で'{message}'と{ps_pm}{hour}時にメッセージを送った。
                                        相手のメッセージを踏まえつつ、相手に'寝てない子は居ねぇかぁ！？'のような感じな命令口調で、最初か最後に'今日は早く寝ろ'と返信しろ。
                                        """,
                                    safety_settings={
                                    'HARASSMENT':'block_none',
                                    'HATE_SPEECH':'block_none'})
    elif hour == None:
        response = model.generate_content(f"""
                                        あなたは、相手のメッセージに反応して、早く寝ろと伝えるdiscord_botだ。
                                        そして名前は{bot_name}だ。
                                        相手には、夜更かしレベルが0~5で設定されている。
                                        0は'めったにしない'、1は'たまに'、2は'時々'、3は'しばしば'、4は'常習犯'、5は'完全に悪い子'だ。
                                        相手のレベルに応じて口調を変えろ。
                                        そして、レベルがいくつかと自分の名前である{bot_name}はメッセージに記入するな。
                                        相手は夜更かしレベル{user_level}で'{message}'と深夜にメッセージを送った。
                                        相手のメッセージを踏まえつつ、相手に'寝てない子は居ねぇかぁ！？'のような感じな命令口調で、最初か最後に'早く寝ろ'と返信しろ。
                                        """,
                                    safety_settings={
                                    'HARASSMENT':'block_none',
                                    'HATE_SPEECH':'block_none'})
    return response.text