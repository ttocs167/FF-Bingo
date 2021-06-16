import numpy as np
from PIL import Image, ImageFont, ImageDraw
from text_wrap import text_wrap
import itertools


def draw_text(img, font, x_coord, y_coord, text):
    draw = ImageDraw.Draw(img)
    draw.text((x_coord, y_coord), text, font=font, align='left', fill=(0, 0, 0, 255), anchor='mm')


def generate_card(image_index, guild, num_images=1, x_cells=5, y_cells=5, free_x=2, free_y=2, beeg=False):
    # number of images to generate and bool to determine if free space is taken from seperate list
    free_space_bool = True

    list_path = "lists/" + guild + "/list.txt"
    free_space_list_path = "lists/" + guild + "/free_list.txt"

    # specify font used
    font_path = r"Montserrat-Regular.ttf"
    font = ImageFont.truetype(font=font_path, size=28)
    # this value determines how the lines are spaced vertically when text is wrapped
    line_height = 22

    # load in the blank bingo card image
    if beeg:
        blank = Image.open("blank_7x7.png")
        blank = blank.convert('RGB')
    else:
        blank = Image.open("blank.png")
        blank.convert('RGB')

    # values of cell spacing on the card
    cell_width = 180

    x_offset = 50  # number of pixels between left edge and start of the bingo grid in the blank
    y_offset = 72  # number of pixels from top of image to top line of the bingo grid in the blank

    # calculate the coords of the centre points of each cell
    x_coords = np.linspace(x_offset + (cell_width//2), (x_offset + (cell_width//2)) + (cell_width*(x_cells-1)), x_cells)
    y_coords = np.linspace(y_offset + (cell_width//2), (y_offset + (cell_width//2)) + (cell_width*(y_cells-1)), y_cells)

    # make a single list of tuples containing all coords
    # this is so the centre square can be popped from a single list
    all_coords = list(itertools.product(x_coords, y_coords))

    if free_space_bool:
        # decide where you want the free space
        free_space = (free_x, free_y)
        # pop the free space coord out of the list
        free_space_coord = all_coords.pop((free_space[0] * x_cells) + free_space[1])

    # loop to generate n random bingo cards
    for image_num in range(num_images):

        image = blank.copy()

        # lists must be loaded every loop for random.choice to resample ¯\_(ツ)_/¯
        # then generate the random values for this card
        statements = np.loadtxt(list_path, dtype=str, comments="#", delimiter="\n", unpack=False)

        if len(statements) < ((x_cells * y_cells) - free_space_bool):
            replace = True
        else:
            replace = False
        random_choices = np.random.choice(statements, (x_cells * y_cells), replace=replace)

        for i in range(len(all_coords)):

            # calculate text wrapping (split into lines with text_wrap() func)
            wrapped_statements = text_wrap(random_choices[i], font, cell_width * 0.9)
            # loop through the splits and place the lines with plt.text()
            for k in range(len(wrapped_statements)):
                draw_text(image, font, all_coords[i][0],
                          (-len(wrapped_statements) * line_height / 2) + all_coords[i][1] + k * line_height,
                          wrapped_statements[k])

        # handle free space text
        if free_space_bool:
            free_statements = np.loadtxt(free_space_list_path, dtype=str, comments="#", delimiter="\n", unpack=False)

            random_free_space = np.random.choice(free_statements, 1, replace=False)
            # write the free space
            wrapped_free_statements = text_wrap(random_free_space[0], font, cell_width * 0.9)
            for k in range(len(wrapped_free_statements)):
                draw_text(image, font, free_space_coord[0],
                          (-len(wrapped_free_statements) * line_height / 2) + free_space_coord[1] + k * line_height,
                          wrapped_free_statements[k])

        if beeg:
            image.save('output_folder/' + guild + '/big_output_' + str(image_index) + '.jpg', "JPEG")
        else:
            image.save('output_folder/' + guild + '/output_' + str(image_index) + '.jpg', "JPEG")

        image_index = (image_index + 1) % 5
