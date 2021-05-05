import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
from text_wrap import text_wrap
import itertools


def draw_text(x_coord, y_coord, text):
    plt.text(x_coord, y_coord, text,
             horizontalalignment='center',
             verticalalignment='center',
             clip_on=True,
             wrap=True,
             size='xx-large')


# number of images to generate and bool to determine if free space is taken from seperate list
num_images = 19
free_space_bool = True

list_path = "list.txt"
free_space_list_path = "free_list.txt"

# specify font used
font_path = r"C:\Windows\Fonts\arial.ttf"
font = ImageFont.truetype(font=font_path, size=30)
# this value determines how the lines are spaced vertically when text is wrapped
line_height = 22
# names on the cards
names = ["Me", "Noah", "Ziggy", "Twink", "Jabber", "Hux", "Fedi", "Robin"]
# load in the blank bingo card image
blank = np.array(Image.open("blank.png"))

# values of cell spacing on the card
cell_width = 180
x_cells = 5
y_cells = 5
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
    free_space = (2, 2)
    # pop the free space coord out of the list
    free_space_coord = all_coords.pop((free_space[0] * x_cells) + free_space[1])

# loop to generate n random bingo cards
for image_num in range(num_images):

    # lists must be loaded every loop for random.choice to resample ¯\_(ツ)_/¯
    # then generate the random values for this card
    statements = np.loadtxt(list_path, dtype=str, comments="#", delimiter="\n", unpack=False)
    random_choices = np.random.choice(statements, (x_cells * y_cells), replace=False)

    # create the plt figure to be drawn on and saved later
    fig = plt.figure(figsize=(14, 14))
    ax = plt.axes(frameon=False, xticks=[], yticks=[])

    for i in range(len(all_coords)):

        # calculate text wrapping (split into lines with text_wrap() func)
        wrapped_statements = text_wrap(random_choices[i], font, cell_width * 0.9)
        # loop through the splits and place the lines with plt.text()
        for k in range(len(wrapped_statements)):
            draw_text(all_coords[i][0],
                      (-len(wrapped_statements) * line_height / 2) + all_coords[i][1] + k * line_height,
                      wrapped_statements[k])

    # handle free space text
    if free_space_bool:
        free_statements = np.loadtxt(free_space_list_path, dtype=str, comments="#", delimiter="\n", unpack=False)
        random_free_space = np.random.choice(free_statements, 1, replace=False)
        # write the free space
        wrapped_free_statements = text_wrap(random_free_space[0], font, cell_width * 0.9)
        for k in range(len(wrapped_free_statements)):
            draw_text(free_space_coord[0],
                      (-len(wrapped_free_statements) * line_height / 2) + free_space_coord[1] + k * line_height,
                      wrapped_free_statements[k])

    if len(names) == num_images:
        # write names on images
        draw_text(900, 988, names[image_num])

    ax.imshow(blank)  # must imshow or figure cannot be saved
    # finally save the output images
    # plt.savefig('output_folder/output_' + str(image_num) + '_.png', bbox_inches='tight', pad_inches=0)
    fig.savefig('output_folder/output_' + str(image_num) + '.png', bbox_inches='tight', pad_inches=0)


