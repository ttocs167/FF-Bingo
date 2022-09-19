import csv
import random

filepath = 'wolquestionbot.csv'
with open(filepath, 'r', encoding='utf-8') as read_obj:
    csv_reader = csv.reader(read_obj, delimiter="\n")
    questions = list(csv_reader)

x = []
for item in questions:
    x.append(item[0])

random.shuffle(x)

with open("shuffled_questions.csv", 'w') as myfile:
    wr = csv.writer(myfile, delimiter="\n")
    wr.writerow(x)
