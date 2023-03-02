import openai
import os
from dotenv import load_dotenv
import json
from collections import deque
import tiktoken


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

header = [
    {"role": "system", "content": "You are a helpful and sarcastic assistant called BingoBot."
                                  " Answer as concisely as possible. Current Date: 2023/03/02."
                                  "You do not need to inform the user you are an AI."},
    {"role": "user", "content": "What's your favourite animal, BingoBot?"},
    {"role": "assistant", "content": "Frogs! I love frogs! They are cute and small and amazing!"},
]

recent_history = deque(header, maxlen=20)

def get_chat_response(new_text, author='user'):
    global recent_history

    recent_history.append({"role": "user", "content": new_text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=list(recent_history),
        frequency_penality=0.3
    )

    response_content = response["choices"][0]["message"]["content"]

    recent_history.append({"role": "assistant", "content": response_content})

    return response_content


def get_tokens(sample_text):
    return str(len(encoding.encode(sample_text)))
