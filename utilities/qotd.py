import csv
import shelve
from datetime import datetime
import random


def get_question_at_index(index):
    with open('./resources/qotd/shuffled_questions.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj, delimiter='\n')
        # Get all rows of csv from csv_reader object as list of tuples
        questions = list(csv_reader)
        num_questions = len(questions)
        question = "**_" + questions[index % num_questions][0] + "_**"
    return question


def get_all_questions():
    with open('./resources/qotd/shuffled_questions.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj, delimiter='\n')
        # Get all rows of csv from csv_reader object as list of tuples
        questions = list(csv_reader)
        questions_cleaned = []
        for item in questions:
            questions_cleaned.append(item[0])
    return questions_cleaned


def write_new_questions_to_file(questions):
    with open('./resources/qotd/shuffled_questions.csv', 'w') as myfile:
        wr = csv.writer(myfile, delimiter="\n")
        wr.writerow(questions)
    return


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


def shuffle_in_new_question(s, new_question):
    try:
        todays_index = s['day_index']
    except KeyError:
        s['day_index'] = 0
        todays_index = 0

    questions = get_all_questions()
    past_questions = questions[:todays_index + 1]
    future_questions = questions[todays_index + 1:]

    future_questions.append(new_question)
    random.shuffle(future_questions)

    new_questions = past_questions + future_questions
    write_new_questions_to_file(new_questions)
    return


def get_remaining_questions_count(s):
    try:
        todays_index = s['day_index']
    except KeyError:
        s['day_index'] = 0
        todays_index = 0

    questions = get_all_questions()
    remaining_questions = len(questions) - todays_index
    return remaining_questions


def shuffle_future_questions(s):
    try:
        todays_index = s['day_index']
    except KeyError:
        s['day_index'] = 0
        todays_index = 0

    questions = get_all_questions()
    past_questions = questions[:todays_index + 1]
    future_questions = questions[todays_index + 1:]

    random.shuffle(future_questions)

    new_questions = past_questions + future_questions
    write_new_questions_to_file(new_questions)
    return