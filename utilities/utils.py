import random
import re
import shutil
import csv
import requests
from difflib import SequenceMatcher
from datetime import datetime
import shelve
import discord

riddle_answer_pairs = []
current_riddle_answer = ""

booba_db = shelve.open("booba.db")
try:
    time_of_last_booba = booba_db['booba_time']
except KeyError:
    print("no booba database found. Creating variable at datetime.now()")
    time_of_last_booba = datetime.now()
    booba_db['booba_time'] = datetime.now()
finally:
    booba_db.close()


def random_animal_emoji():
    emojis = [":frog:", ":pig:", ":rabbit:", ":dog:", ":cat:", ":mouse:", ":hamster:", ":fox:", ":bear:",
              ":panda_face:", ":hatching_chick:", ":chicken:", ":penguin:"]

    choice = random.choice(emojis)

    return choice


def random_8ball_response():
    responses = ["Yes", "No", "Maybe", "Certainly", "Surely not", "Of Course", "No way",
                 "Who Cares?", "Fo Sho Dawg", ":frog:"]
    choice = random.choices(responses, weights=[1, 1, 1, 1, 1, 1, 1, .5, .5, .05])[0]

    output = "_**" + choice + "**_"

    return output


def random_compliment():
    compliments = ["You look lovely today :)", "Treat yourself!", "<3", "You're great", "Keep it up",
                   "You dont look a day over [CURRENT_AGE - 5] :)", "You are who you are", "Never change!",
                   "We're all better off with you around :)", "You're worth more than you give yourself credit for",
                   "You are your own worst critic", "Love yourself more, you are worth that and more",
                   "You probably shouldn't seek self validation from a discord bot, but for what its worth,"
                   " I think you're amazing", "You can do anything if you try",
                   "Give yourself a break every now and then", "__hugs__", "Mistakes just mean you're trying!"]

    choice = random.choices(compliments)[0]

    output = "_**" + choice + "**_"
    return output


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
    chunks = [lines[x:x + 50] for x in range(0, len(lines), 50)]

    return chunks


async def list_all_free_lines(guild):
    with open("lists/" + guild + "/free_list.txt", 'r') as file:
        lines = list(enumerate(file.readlines()))

    lines = [item for sublist in lines for item in sublist]
    lines = list(map(str, lines))
    chunks = [lines[x:x + 50] for x in range(0, len(lines), 50)]

    return chunks


async def get_line(index, guild):
    with open("lists/" + guild + "/list.txt", "r") as infile:
        lines = infile.readlines()
    return lines[index]


async def get_free_line(index, guild):
    with open("lists/" + guild + "/free_list.txt", "r") as infile:
        lines = infile.readlines()
    return lines[index]


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
    try:
        shutil.copy("lists/" + guild + "/list.txt", "lists/" + guild + "/list_OLD.txt")
    except Exception:
        print("There is no old list to backup. New server being initialised.")

    with open("./lists/default_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/list.txt", "w") as file:
        for line in default_lines:
            file.write(line)


async def reset_free_list(guild):
    try:
        shutil.copy("lists/" + guild + "/free_list.txt", "lists/" + guild + "/free_list_OLD.txt")
    except Exception:
        print("There is no old free list to backup. New server being initialised.")

    with open("./lists/default_free_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/free_list.txt", "w") as file:
        for line in default_lines:
            file.write(line)


def load_riddles():
    global riddle_answer_pairs

    with open('./resources/riddles/more riddles.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Get all rows of csv from csv_reader object as list of tuples
        list_of_tuples = list(map(tuple, csv_reader))
        riddle_answer_pairs = list_of_tuples

    print("riddles loaded!")

    return


async def random_riddle_answer():
    global current_riddle_answer

    pair = random.choice(riddle_answer_pairs)
    riddle, answer = str(pair[0]), str(pair[1])
    answer = answer.strip(" \"")
    out = "_" + riddle + "_" + "\n" + pad_spoiler_with_spaces(answer)

    current_riddle_answer = answer
    return out


async def check_riddle(text):
    global current_riddle_answer
    if SequenceMatcher(None, text.lower(), current_riddle_answer.lower()).ratio() > 0.8:
        return True
    else:
        return False


def random_wipe_reason(caller):
    reasons = ["Tank", "Off-Tank", "DPS", "Healer", "@" + caller, "🐸"]
    weights = [1, 1, 1, 1, 1, 0.05]
    reason = random.choices(reasons, weights=weights)[0]
    if reason == "@" + caller:
        return "_It was the **" + "<" + reason + ">" + "**_"
    output = "_It was the **" + reason + "**_"
    return output


def booba(member: discord.Member):
    def ordinal(n):
        return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

    time_since_last_booba = datetime.now() - time_of_last_booba

    days = time_since_last_booba.days
    hours = time_since_last_booba.seconds // 3600
    minutes = (time_since_last_booba.seconds // 60) % 60
    seconds = time_since_last_booba.seconds % 60

    s = shelve.open('booba.db')
    try:
        booba_offenders = s['offenders']
    except KeyError:
        s['offenders'] = {}
        booba_offenders = s['offenders']

    try:
        booba_offenders[member.id] += 1
        offense_num = booba_offenders[member.id]
    except KeyError:
        booba_offenders[member.id] = 1
        offense_num = 1

    s['offenders'] = booba_offenders

    if member.nick is not None:
        name = member.nick
    else:
        name = member.name

    offender_text = "This is {}'s **{}** offense.".format(name, ordinal(offense_num))

    s.close()

    return days, hours, minutes, seconds, offender_text


def reset_booba():
    global time_of_last_booba
    s = shelve.open('booba.db')
    try:
        s['booba_time'] = datetime.now()
        time_of_last_booba = datetime.now()
    finally:
        s.close()


async def booba_board(ctx):
    s = shelve.open('booba.db')
    try:
        booba_offenders = s['offenders']
    except KeyError:
        s['offenders'] = {}
        booba_offenders = s['offenders']

    s.close()

    sorted_offenders = {k: v for k, v in sorted(booba_offenders.items(), key=lambda item: item[1], reverse=True)}

    output = "**Booba reset leaderboard!**\n"

    for key in sorted_offenders:
        user_id = key
        offenses = sorted_offenders[key]
        member = await ctx.guild.fetch_member(user_id)
        name = member.nick
        if name is None:
            name = member.name
        output += "**" + name + ": {}".format(offenses) + "**\n"

    return output


def yolo_response(img_url):
    DETECTION_URL = "http://localhost:5000/v1/object-detection/yolov5s"
    response = requests.post(DETECTION_URL, json={"image_url": img_url})

    if response.status_code == 200:
        img_path = "./yolo/out.jpg"
        return img_path
    return ""


def pad_spoiler_with_spaces(text):
    if len(text) < 10:
        for _ in range(10 - len(text)):
            text += " "
    out = "||" + text + "||"
    return out


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
