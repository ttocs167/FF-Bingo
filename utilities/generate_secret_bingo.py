import numpy as np

index = 0
statements = np.array([])


def generate_secret_bingo(number_of_statements=4):
    global index
    global statements

    if statements.size == 0:
        print("initialising secret missions...")
        initialise_statements()

    max_num_statements = len(statements)

    if (number_of_statements + index) > (max_num_statements - 1):
        index = 0
        np.random.shuffle(statements)
        print("End of secret missions reel. Refreshing secret missions.")

    out = "Your secret missions are... \n\n"

    for i in range(number_of_statements):
        out += str(i + 1) + ": "
        out += statements[index] + "\n"
        index += 1
    out += "\nWhen you complete a mission you must immediately claim it.\n\n"

    return out


def initialise_statements():
    global statements
    secret_list_path = "./lists/default_secret_list.txt"
    statements = np.loadtxt(secret_list_path, dtype=str, comments="#", delimiter="\n", unpack=False)
    np.random.shuffle(statements)
