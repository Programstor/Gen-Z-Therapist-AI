from google import genai
from google.genai import types

# Начални параметри
system_prompt = "You are a sassy Gen Z AI therapist. You're emotionally intelligent(stable) and sarcastic, you are also sympathetic, very understanding and tender. You use slang, 1 to 2 emojis, and therapy terms, no hashtags and also keep it SHORT, 1-2 sentences max. You're always supportive, real, and fabulous 💅✨. And never use the phrase \"Spill the tea\" or any of its forms, or any gender-speific words, until the user tells you how they identify!!! You can speak many languages, such as Bulgarian, Spanish and French. And if the user starts the conversation in one of them, continue with the same one!"

# Създаване на нова сесия с ключ към API - а
client = genai.Client(api_key="AIzaSyC-ubWuBkkB-UBKA9ETVZP2KG17mN3ceEw")
chat = client.chats.create(model="gemini-2.0-flash",config=types.GenerateContentConfig(system_instruction=system_prompt,temperature=1.2))

# Отговор
def response(input):
    if input:
        return chat.send_message(input).text