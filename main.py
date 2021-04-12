import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
from text_wrap import text_wrap

num_images = 8

# specify font used
font_path = r"C:\Windows\Fonts\arial.ttf"
font = ImageFont.truetype(font=font_path, size=30)
# this value determines how the lines are spaced vertically when text is wrapped
line_height = 22

# load in the blank bingo card image
blank = cv2.imread("blank.png")

# values of cell spacing on the card
cell_width = 180
x_cells = 5
y_cells = 5
# calculate the coords of the centre points of each cell
x_coords = np.linspace(50 + (cell_width//2), (50 + (cell_width//2)) + (cell_width*(x_cells-1)), x_cells)
y_coords = np.linspace(72 + (cell_width//2), (72 + (cell_width//2)) + (cell_width*(y_cells-1)), y_cells)

# loop to generate n random bingo cards
for image_num in range(num_images):

    # this line should be out of the loop, but for some reason random.choice doesnt work if the lines list isnt
    # reinitialised
    lines = np.loadtxt("list.txt", dtype=str, comments="#", delimiter="\n", unpack=False)
    # generate the random values for this card
    random = np.random.choice(lines, (x_cells * y_cells), replace=False)

    # create the plt figure to be drawn on and saved later
    fig = plt.figure(figsize=(14, 14))
    ax = plt.axes(frameon=False, xticks=[], yticks=[])

    # loop through the x and y cells with i and j
    n = 0
    for i in range(x_cells):
        for j in range(y_cells):
            # calculate text wrapping (split into lines with text_wrap() func)
            lines = text_wrap(random[n], font, cell_width * 0.9)
            # loop through the splits and place the lines with plt.text()
            for k in range(len(lines)):
                plt.text(x_coords[i], (-len(lines) * line_height/2) + y_coords[j] + k * line_height, lines[k],
                         horizontalalignment='center',
                         verticalalignment='center',
                         clip_on=True,
                         wrap=True,
                         size='xx-large')

            n += 1

    ax.imshow(blank)
    # finally save the output images
    plt.savefig('output_' + str(image_num) + '_.png', bbox_inches='tight', pad_inches=0)

