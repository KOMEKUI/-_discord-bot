from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv(dotenv_path="token.env")

GOOGLE_API_KEY= os.getenv("Gemini_TOKEN")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def create_message(target_message):
    response = model.generate_content(f"あなたは、相手のメッセージに反応して、早く寝ろと伝えるdiscordのbotだ。相手は'{target_message}'とメッセージを送った。相手に'寝てない子は居ねぇかぁ！？'のような感じな命令口調で、最初か最後に'早く寝ろ'と言え。文の終わりに一回改行しろ。",
                                safety_settings={
								'HARASSMENT':'block_none',
                                'HATE_SPEECH':'block_none'})
    return response.text