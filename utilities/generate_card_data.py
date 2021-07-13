import numpy as np
import json


def generate_card_data(guild, x_cells=5, y_cells=5, free_x=2, free_y=2, beeg=False):
    # number of images to generate and bool to determine if free space is taken from seperate list
    free_space_bool = True

    list_path = "./lists/" + guild + "/list.txt"
    free_space_list_path = "./lists/" + guild + "/free_list.txt"

    # then generate the random values for this card
    statements = np.loadtxt(list_path, dtype=str, comments="#", delimiter="\n", unpack=False)
    if len(statements) < ((x_cells * y_cells) - free_space_bool):
        replace = True
    else:
        replace = False
    random_choices = np.random.choice(statements, (x_cells * y_cells), replace=replace)

    # handle free space text
    random_free_space = []
    if free_space_bool:
        free_statements = np.loadtxt(free_space_list_path, dtype=str, comments="#", delimiter="\n", unpack=False)
        random_free_space = np.random.choice(free_statements, 1, replace=False)
        # write the free space

    data = json.dumps({"spaces": list(random_choices),
                       "free_spaces": list(random_free_space),
                       "dimensions": [x_cells, y_cells],
                       "free space coordinates": [free_x, free_y]})

    return data
