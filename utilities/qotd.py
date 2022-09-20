import csv
import shelve
from datetime import datetime


def get_question_at_index(index):
    with open('./resources/qotd/shuffled_questions.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj, delimiter='\n')
        # Get all rows of csv from csv_reader object as list of tuples
        questions = list(csv_reader)
        num_questions = len(questions)
        question = "**_" + questions[index % num_questions][0] + "_**"
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


def get_todays_question(s):

    try:
        todays_index = s['day_index']
    except KeyError:
        s['day_index'] = 0
        todays_index = 0

    question = get_question_at_index(todays_index)
    return question
