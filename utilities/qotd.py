import csv
import shelve
from datetime import datetime


def get_question_at_index(index):
    with open('./resources/qotd/questions.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Get all rows of csv from csv_reader object as list of tuples
        questions = list(csv_reader)
        num_questions = len(questions)
        question = "**__" + questions[index % num_questions][0] + "__**"
    return question


async def enable_qotd(channel_id):
    s = shelve.open('qotd.db')
    try:
        channels = s['enabled_channels']
        if channel_id not in channels:
            channels.append(channel_id)
            s['enabled_channels'] = channels
    finally:
        s.close()
    return


async def disable_qotd(channel_id):
    s = shelve.open('qotd.db')
    try:
        channels = s['enabled_channels']
        if channel_id in channels:
            channels.remove(channel_id)
            s['enabled_channels'] = channels
    finally:
        s.close()
    return


def get_todays_question():
    s = shelve.open('qotd.db')
    try:
        todays_index = s['day_index']
        s['day_index'] += 1
    except KeyError:
        s['day_index'] = 0
        todays_index = 0
    finally:
        s.close()

    question = get_question_at_index(todays_index)
    return question


def get_channels():
    s = shelve.open('qotd.db')
    channels = s['enabled_channels']
    s.close()
    return channels
