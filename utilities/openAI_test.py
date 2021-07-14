import openai
import os
from dotenv import load_dotenv
import json
from collections import deque

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nBingoBot:"
restart_sequence = "\nHuman: "

prompt_header = "The following is a conversation with an AI assistant called BingoBot and a chat room of friends. " \
                "BingoBot is helpful, creative, clever, kind, supporting and very friendly." \
                "\n\nHuman: Hello, who are you?" \
                "\nBingoBot: I am BingoBot, an AI assistant here to help and entertain you!"

recent_history = deque([], maxlen=10)

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


def get_ai_response(new_text, author='Human'):
    global recent_history

    recent_history.append("\n" + author + ": " + new_text + "\nBingoBot: ")

    response = openai.Completion.create(
        engine="curie",
        prompt=prompt_header + ''.join(recent_history),
        temperature=0.9,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", "Human:", "BingoBot"]
    )

    response = json.loads(json.dumps(response))

    response_text = response['choices'][0]['text']

    recent_history.append(response_text)

    print(recent_history)

    return response_text
