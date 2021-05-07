import random
import re
import itertools


def random_animal_emoji():
    emojis = [":frog:", ":pig:", ":rabbit:", ":dog:", ":cat:", ":mouse:", ":hamster:", ":fox:", ":bear:",
              ":panda_face:", ":hatching_chick:", ":chicken:", ":penguin:"]

    choice = random.choice(emojis)

    return choice


async def add_to_list(new_line, guild):
    with open("lists/" + guild + "/list.txt", 'a') as file:
        file.writelines(new_line + "\n")


async def add_to_free_list(new_line, guild):
    with open("lists/" + guild + "/free_list.txt", 'a') as file:
        file.writelines(new_line + "\n")


async def list_all_lines(guild):
    with open("lists/" + guild + "/list.txt", 'r') as file:
        lines = list(enumerate(file.readlines()))

    lines = [item for sublist in lines for item in sublist]
    lines = list(map(str, lines))
    chunks = [lines[x:x+50] for x in range(0, len(lines), 50)]

    return chunks


async def list_all_free_lines(guild):
    with open("lists/" + guild + "/free_list.txt", 'r') as file:
        lines = list(enumerate(file.readlines()))

    lines = [item for sublist in lines for item in sublist]
    lines = list(map(str, lines))
    chunks = [lines[x:x + 50] for x in range(0, len(lines), 50)]

    return chunks


async def delete_line(index, guild):
    with open("lists/" + guild + "/list.txt", "r") as infile:
        lines = infile.readlines()

    if index <= len(lines):
        with open("lists/" + guild + "/list.txt", "w") as outfile:
            for pos, line in enumerate(lines):
                if pos != index:
                    outfile.write(line)


async def delete_free_line(index, guild):
    with open("lists/" + guild + "/free_list.txt", "r") as infile:
        lines = infile.readlines()

    if index <= len(lines):
        with open("lists/" + guild + "/free_list.txt", "w") as outfile:
            for pos, line in enumerate(lines):
                if pos != index:
                    outfile.write(line)


async def reset_list(guild):
    with open("lists/default_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/list.txt", "w") as file:
        for line in default_lines:
            file.write(line)


async def reset_free_list(guild):
    with open("lists/default_free_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/free_list.txt", "w") as file:
        for line in default_lines:
            file.write(line)


def emoji_free_text(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U0001F1F2-\U0001F1F4"  # Macau flag
                               u"\U0001F1E6-\U0001F1FF"  # flags
                               u"\U0001F600-\U0001F64F"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U0001F1F2"
                               u"\U0001F1F4"
                               u"\U0001F620"
                               u"\u200d"
                               u"\u2640-\u2642"
                               "]+", flags=re.UNICODE)

    text = emoji_pattern.sub(r'', text)
    return text


