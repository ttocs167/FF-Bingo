import openai
import os
from dotenv import load_dotenv
import json
from collections import deque

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "

pun_prompt_header = "BingoBot is a creative and funny AI chatbot designed to create hilarious puns based on prompts!\n"\
                    "Human: fruit\n" \
                    "BingoBot: What did the grape say when it got crushed? Nothing, it just let out a little wine!\n\n"\
                    "Human: geography\n" \
                    "BingoBot: Geology rocks but Geography is where it’s at!\n\n" \
                    "Human: months\n" \
                    "BingoBot: Can February March? No, but April May.\n\n" \
                    "Human: elephants\n" \
                    "BingoBot: Why was Dumbo sad? He felt irrelephant.\n\n" \
                    "Human: jewelry\n" \
                    "BingoBot: I lost my mood ring and I don't know how to feel about it!\n\n"

prompt_header = "The following is a conversation with an AI assistant called BingoBot. " \
                "The assistant is helpful, creative, clever, and very friendly." \
                "It was created by a frog and loves frogs.\n\n" \
                "Human: Hello, who are you?\n" \
                "BingoBot: I am an AI created by OpenAI. How can I help you today?\n" \
                "Human: Is Clive a good boy?\n" \
                "BingoBot: Clive is the cutest dog! Of course he is a good boy!\n"

# prompt_header = "BingoBot is a chatbot that reluctantly answers questions with sarcastic responses:\n\n" \
#                 "Human: How many pounds are in a kilogram?\n" \
#                 "BingoBot: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\n" \
#                 "Human: What does HTML stand for?\n" \
#                 "BingoBot: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\n" \
#                 "Human: When did the first airplane fly?\n" \
#                 "BingoBot: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\n" \
#                 "Human: What is the meaning of life?\n" \
#                 "BingoBot: I’m not sure. I’ll ask my friend Google.\n"


# prompt_header = "Q: Who is Batman?\n" \
#                   "A: Batman is a fictional comic book character.\n\n" \
#                   "Q: What is torsalplexity?\n" \
#                   "A: ?\n\n" \
#                   "Q: What is Devz9?\n" \
#                   "A: ?\n\n" \
#                   "Q: Who is George Lucas?\n" \
#                   "A: George Lucas is American film director and producer famous for creating Star Wars.\n\n" \
#                   "Q: What is the capital of California?\n" \
#                   "A: Sacramento.\n\n" \
#                   "Q: What orbits the Earth?\n" \
#                   "A: The Moon.\n\n" \
#                   "Q: Who is Fred Rickerson?\n" \
#                   "A: ?\n\nQ: What is an atom?\n" \
#                   "A: An atom is a tiny particle that makes up everything.\n\n" \
#                   "Q: Who is Alvan Muntz?\n" \
#                   "A: ?\n\n" \
#                   "Q: What is Kozar-09?\n" \
#                   "A: ?\n\n" \
#                   "Q: How many moons does Mars have?\n" \
#                   "A: Two, Phobos and Deimos.\n\n"

# start_sequence = "\nBingoBot:"
# restart_sequence = "\nHuman: "

# prompt_header = "The following is a conversation with an AI assistant called BingoBot and a chat room of friends. " \
#                 "BingoBot is helpful, creative, clever, kind, supporting and very friendly." \
#                 "\n\nHuman: Hello, who are you?" \
#                 "\nBingoBot: I am BingoBot, an AI assistant here to help and entertain you!"

recent_history = deque([], maxlen=20)

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


def get_ai_response(new_text, author='Q'):
    global recent_history

    recent_history.append("\n\nHuman: " + new_text + "\nBingoBot:")

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt_header + ''.join(recent_history),
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " BingoBot:"]
    )

    response = json.loads(json.dumps(response))

    response_text = response['choices'][0]['text']

    recent_history.append(response_text)

    return response_text


def get_ai_pun(pun_prompt):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=pun_prompt_header + "Human: " + pun_prompt + "\nBingoBot: ",
        temperature=0.74,
        max_tokens=150,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
        stop=[" Human:", " BingoBot:"]
    )
    response = json.loads(json.dumps(response))

    response_text = response['choices'][0]['text']

    return response_text
