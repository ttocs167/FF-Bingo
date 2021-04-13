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


num_images = 8

# specify font used
font_path = r"C:\Windows\Fonts\arial.ttf"
font = ImageFont.truetype(font=font_path, size=30)
# this value determines how the lines are spaced vertically when text is wrapped
line_height = 22

# load in the blank bingo card image
blank = np.array(Image.open("blank.png"))

# values of cell spacing on the card
cell_width = 180
x_cells = 5
y_cells = 5

# calculate the coords of the centre points of each cell
x_coords = np.linspace(50 + (cell_width//2), (50 + (cell_width//2)) + (cell_width*(x_cells-1)), x_cells)
y_coords = np.linspace(72 + (cell_width//2), (72 + (cell_width//2)) + (cell_width*(y_cells-1)), y_cells)

# make a single list of tuples containing all coords
all_coords = list(itertools.product(x_coords, y_coords))

# decide where you want the free space
free_space = (2, 2)
# pop the free space coord out of the list
free_space_coord = all_coords.pop((free_space[0] * x_cells) + free_space[1])

statements = np.loadtxt("list.txt", dtype=str, comments="#", delimiter="\n", unpack=False)
free_statements = np.loadtxt("free_list.txt", dtype=str, comments="#", delimiter="\n", unpack=False)

# loop to generate n random bingo cards
for image_num in range(num_images):

    # generate the random values for this card
    random_choices = np.random.choice(statements, (x_cells * y_cells), replace=False)
    random_free_space = np.random.choice(free_statements, 1, replace=False)

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

    # write the free space
    wrapped_free_statements = text_wrap(random_free_space[0], font, cell_width * 0.9)
    for k in range(len(wrapped_free_statements)):
        draw_text(free_space_coord[0],
                  (-len(wrapped_free_statements) * line_height / 2) + free_space_coord[1] + k * line_height,
                  wrapped_free_statements[k])

    ax.imshow(blank)
    # finally save the output images
    plt.savefig('output_' + str(image_num) + '_.png', bbox_inches='tight', pad_inches=0)


