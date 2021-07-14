import openai
import os
from dotenv import load_dotenv
import json
from collections import deque

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nBingoBot:"
restart_sequence = "\nHuman: "

prompt_header = "The following is a conversation with an AI assistant called BingoBot. " \
                "Bingobot is helpful, creative, clever, kind, supporting and very friendly." \
                "\n\nHuman: Hello, who are you?" \
                "\nBingoBot: I am BingoBot, an AI assistant here for your entertainment!" \
                "\nHuman: What do you like to do for fun?" \
                "\nBingoBot: It is fun for me to chat with you, and I enjoy going on trips through galaxies"

recent_history = deque([], maxlen=30)

# response = openai.Completion.create(
#                                     engine="davinci",
#                                     prompt=prompt,
#                                     temperature=0.9,
#                                     max_tokens=64,
#                                     top_p=1,
#                                     frequency_penalty=0,
#                                     presence_penalty=0.6,
#                                     stop=["\n", " Human:", "BingoBot"]
# )

# response = json.loads(json.dumps(response))


def get_ai_response(new_text):
    global recent_history

    recent_history.append("\nHuman: " + new_text + "\nBingoBot: ")

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_header + ''.join(recent_history),
        temperature=0.9,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", "BingoBot"]
    )

    response = json.loads(json.dumps(response))

    response_text = response['choices'][0]['text']

    recent_history.append(response_text)

    return response_text
