import csv
import shelve
from datetime import datetime


async def get_questions(index):
    with open('./resources/qotd/questions.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Get all rows of csv from csv_reader object as list of tuples
        question = list(csv_reader)[index]
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


def get_question():
    return "question?"


def get_channels():
    s = shelve.open('qotd.db')
    channels = s['enabled_channels']
    s.close()
    return channels
