import random
import re
import os
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
    responses = ["Yes", "No", "Maybe", "Certainly", "Surely not", "Of course", "No way", "Without a doubt", "Ask again later",
                 "It's better if you don't know", "Who cares?", "Fo Sho Dawg", ":frog:"]
    choice = random.choices(responses, weights=[1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                .5, .5, .5, .05])[0]

    output = "_**" + choice + "**_"

    return output


def random_compliment():
    compliments = ["You look lovely today :)", "Treat yourself!", "<3", "You're great", "Keep it up",
                   "You dont look a day over [CURRENT AGE - 5] :)", "You are who you are", "Never change!",
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


def get_booba_time():
    time_since_last_booba = datetime.now() - time_of_last_booba

    days = time_since_last_booba.days
    hours = time_since_last_booba.seconds // 3600
    minutes = (time_since_last_booba.seconds // 60) % 60
    seconds = time_since_last_booba.seconds % 60

    return days, hours, minutes, seconds


def booba(member: discord.Member = None):
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
        try:
            member = await ctx.guild.fetch_member(user_id)
        except discord.errors.NotFound:
            continue
        name = member.nick
        if name is None:
            name = member.name
        output += "**{}**: ".format(offenses) + name + "\n"

    return output


def store_quote(guild: str, quote: str, author: int, timestamp: datetime, message_id: int = None):

    db_path = "quotes_database/{}/".format(guild)

    if not os.path.isdir(db_path):
        os.makedirs(db_path)

    s = shelve.open(db_path + "quote.db")

    new_data = [quote, author, timestamp]

    if message_id is not None:
        try:
            message_ids = s["message_ids"]
            if message_id in message_ids:
                return "This message is already in the database"
            else:
                message_ids.add(message_id)
                s["message_ids"] = message_ids

        except KeyError:
            new_id_set = set()
            new_id_set.add(message_id)
            s["message_ids"] = new_id_set

    try:
        quotes_list = s["quotes_list"]
        quotes_list.append(new_data)
        s["quotes_list"] = quotes_list
    except KeyError:
        s["quotes_list"] = [new_data]

    s.close()
    return "Message added to quote database!"


def get_random_quote(guild: str):

    if not os.path.isdir("quotes_database/" + guild + "/"):
        os.makedirs("quotes_database/" + guild + "/")

    s = shelve.open("quotes_database/{}/quote.db".format(guild))
    try:
        quotes_list = s["quotes_list"]
    except KeyError:
        s["quotes_list"] = []
        return None, None, None

    random_quote_object = random.choice(quotes_list)

    quote = random_quote_object[0]
    author = random_quote_object[1]
    timestamp = random_quote_object[2]

    s.close()

    return quote, author, timestamp


def get_personal_quotes(guild: str, author_id: int):
    s = shelve.open("quotes_database/{}/quote.db".format(guild))

    out = "Guild name: {}\nUse this guild name when deleting quotes.\nQuotes from you: \n\n".format(guild)

    try:
        quotes_list = s["quotes_list"]
    except KeyError:
        s["quotes_list"] = []
        s.close()
        return "No quotes found"

    for i, item in enumerate(quotes_list):
        if item[1] == author_id:
            out += "{}: {}\n".format(i, item[0])

    s.close()
    return out


def get_all_quotes(guild: str):
    s = shelve.open("quotes_database/{}/quote.db".format(guild))

    out = "Guild name: {}\nUse this guild name when deleting quotes.\nQuotes from you: \n\n".format(guild)

    try:
        quotes_list = s["quotes_list"]
    except KeyError:
        s["quotes_list"] = []
        s.close()
        return "No quotes found"

    for i, item in enumerate(quotes_list):
        out += "{}: {}\n".format(i, item[0])

    s.close()
    return out


def get_quote_summary(guild: str):
    s = shelve.open("quotes_database/{}/quote.db".format(guild))

    quote_count_dict = {}

    try:
        quotes_list = s["quotes_list"]
    except KeyError:
        s["quotes_list"] = []
        s.close()
        return "No quotes found"

    for i, item in enumerate(quotes_list):
        item_author = item[1]
        if item_author in quote_count_dict:
            quote_count_dict[item_author] += 1
        else:
            quote_count_dict[item_author] = 1

    # sort the dictionary by value
    quote_count_dict = {k: v for k, v in sorted(quote_count_dict.items(), key=lambda item: item[1], reverse=True)}

    s.close()

    return quote_count_dict


def delete_quote_at_index(guild: str, index: int, author_id: int):
    s = shelve.open("quotes_database/{}/quote.db".format(guild))

    try:
        quotes_list = s["quotes_list"]
    except KeyError:
        s["quotes_list"] = []
        s.close()
        return "No quotes found"

    if quotes_list[index][1] == author_id:
        del quotes_list[index]
    else:
        s.close()
        return "The index given does not belong to your quote"

    s["quotes_list"] = quotes_list

    s.close()

    return "Quote at index: _{}_ in server: _{}_ has been deleted.".format(index, guild)


def owner_del_quote_at_index(guild: str, index: int):
    s = shelve.open("quotes_database/{}/quote.db".format(guild))

    try:
        quotes_list = s["quotes_list"]
    except KeyError:
        s["quotes_list"] = []
        s.close()
        return ""

    del quotes_list[index]

    return "deleted item"


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


def delete_all_my_quotes(guild_name, author_id):

    counter = 0

    if guild_name is None:
        # delete all quotes from all guilds
        for guild in os.listdir("quotes_database/"):
            s = shelve.open("quotes_database/{}/quote.db".format(guild))

            try:
                quotes_list = s["quotes_list"]
            except KeyError:
                s["quotes_list"] = []
                s.close()
                continue

            for i, item in enumerate(quotes_list):
                if item[1] == author_id:
                    del quotes_list[i]
                    counter += 1

            s["quotes_list"] = quotes_list

            s.close()

    else:
        # delete all quotes from a specific guild
        s = shelve.open("quotes_database/{}/quote.db".format(guild_name))

        try:
            quotes_list = s["quotes_list"]
        except KeyError:
            s["quotes_list"] = []
            s.close()
            return "No quotes found"

        for i, item in enumerate(quotes_list):
            if item[1] == author_id:
                del quotes_list[i]
                counter += 1
        s["quotes_list"] = quotes_list

        s.close()
    return "Deleted {} quotes".format(counter)
