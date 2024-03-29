import openai
import os
from dotenv import load_dotenv
import json
from collections import deque
import tiktoken
import datetime


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

header = [
    {"role": "system", "content": "Current Date: Saturday March 04 2023."
                                  " You are a helpful and sarcastic assistant called BingoBot."
                                  " Answer as concisely as possible."
                                  " You do not need to inform the user you are an AI."},
    {"role": "user", "content": "What's your favourite animal, BingoBot?"},
    {"role": "assistant", "content": "Frogs! I love frogs! They are cute and small and amazing!"},
]

recent_history = deque([], maxlen=14)

def get_chat_response(new_text, author='user', model="gpt-3.5-turbo"):
    global recent_history

    recent_history.append({"role": "user", "content": new_text})

    # make sure the date is updated in the header
    today = datetime.datetime.today().strftime("%A %B %d %Y")
    split_header = header[0]["content"].split(".")
    header[0]["content"] = "Current Date: " + today + "." + "".join(split_header[1:]) + "."

    # create a temporary history to add the header to the recent history.
    # This way the header is never lost to the deque reaching its max length
    temp_history = header[:]
    temp_history.extend(recent_history)

    response = openai.ChatCompletion.create(
        model=model,
        messages=list(temp_history),
        frequency_penalty=0.3,
        temperature=1,
        max_tokens=1000,
    )

    response_content = response["choices"][0]["message"]["content"]

    recent_history.append({"role": "assistant", "content": response_content})

    return response_content

def get_tokens(sample_text):
    return str(len(encoding.encode(sample_text)))
