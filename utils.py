import random


def random_animal_emoji():
    emojis = [":frog:", ":pig:", ":rabbit:", ":dog:", ":cat:", ":mouse:", ":hamster:", ":fox:", ":bear:",
              ":panda_face:", ":hatching_chick:", ":chicken:", ":penguin:"]

    choice = random.choice(emojis)

    return choice


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
        lines = ' '.join(list(map(str, lines)))
    return lines


async def list_all_free_lines(guild):
    with open("lists/" + guild + "/free_list.txt", 'r') as file:
        lines = list(enumerate(file.readlines()))
        lines = [item for sublist in lines for item in sublist]
        lines = ' '.join(list(map(str, lines)))
    return lines


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
    with open("lists/default_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/list.txt", "w") as file:
        for line in default_lines:
            file.write(line)


async def reset_free_list(guild):
    with open("lists/default_free_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/free_list.txt", "w") as file:
        for line in default_lines:
            file.write(line)
