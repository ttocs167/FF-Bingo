import openai
import os
from dotenv import load_dotenv
import json
from collections import deque

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "

prompt_header = "I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth," \
                " I will give you the answer. If you ask me a question that is nonsense," \
                " trickery, or has no clear answer, I will respond with \"Unknown\".\n\n" \
                "Q: What is human life expectancy in the United States?\n" \
                "A: Human life expectancy in the United States is 78 years.\n\n" \
                "Q: Who was president of the United States in 1955?\n" \
                "A: Dwight D. Eisenhower was president of the United States in 1955.\n\n" \
                "Q: Which party did he belong to?\n" \
                "A: He belonged to the Republican Party.\n\n" \
                "Q: What is the square root of banana?\n" \
                "A: Unknown\n\n" \
                "Q: How does a telescope work?\n" \
                "A: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\n" \
                "Q: Where were the 1992 Olympics held?\n" \
                "A: The 1992 Olympics were held in Barcelona, Spain.\n\n" \
                "Q: How many squigs are in a bonk?\n" \
                "A: Unknown"

# start_sequence = "\nBingoBot:"
# restart_sequence = "\nHuman: "

# prompt_header = "The following is a conversation with an AI assistant called BingoBot and a chat room of friends. " \
#                 "BingoBot is helpful, creative, clever, kind, supporting and very friendly." \
#                 "\n\nHuman: Hello, who are you?" \
#                 "\nBingoBot: I am BingoBot, an AI assistant here to help and entertain you!"

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

    recent_history.append("\n\nQ: " + new_text + "\nA:")

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_header + ''.join(recent_history),
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )

    response = json.loads(json.dumps(response))

    response_text = response['choices'][0]['text']

    recent_history.append(response_text)

    print(''.join(recent_history))

    return response_text
