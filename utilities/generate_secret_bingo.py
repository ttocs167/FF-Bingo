import numpy as np


def generate_secret_bingo(guild, number_of_statements=4):
    secret_list_path = "./lists/" + guild + "/secret_list.txt"

    statements = np.loadtxt(secret_list_path, dtype=str, comments="#", delimiter="\n", unpack=False)

    try:
        random_choices = np.random.choice(statements, number_of_statements, replace=False)
    except:
        print("SECRET BINGO: reset random choice")
        statements = np.loadtxt(secret_list_path, dtype=str, comments="#", delimiter="\n", unpack=False)
        random_choices = np.random.choice(statements, number_of_statements, replace=False)

    out = "Your secret missions are... \n\n"

    for i, secret_mission in enumerate(random_choices):
        out += str(i + 1) + ": "
        out += secret_mission + "\n"

    out += "When you complete a mission you must immediately claim it.\n\n"

    return out
