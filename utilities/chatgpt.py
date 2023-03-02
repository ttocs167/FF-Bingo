import openai
import os
from dotenv import load_dotenv
import json
from collections import deque

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

header = [
    {"role": "system", "content": "You are a helpful and sarcastic assistant called BingoBot."},
    {"role": "user", "content": "What's your favourite animal, BingoBot?"},
    {"role": "assistant", "content": "Frogs! I love frogs! They are cute and small and amazing!"},
]

recent_history = deque(header, maxlen=20)

def get_chat_response(new_text):
    global recent_history

    recent_history.append({"role": "user", "content": new_text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=list(recent_history)
    )

    response_content = response["choices"][0]["message"]["content"]

    recent_history.append({"role": "assistant", "content": response_content})

    return response
