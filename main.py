import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
from text_wrap import text_wrap

num_images = 8

font_path = r"C:\Windows\Fonts\arial.ttf"
font = ImageFont.truetype(font=font_path, size=30)
line_height = 22

blank = cv2.imread("blank.png")

cell_width = 180
x_cells = 5
y_cells = 5
x_coords = np.linspace(50 + (cell_width//2), (50 + (cell_width//2)) + (cell_width*(x_cells-1)), x_cells)
y_coords = np.linspace(72 + (cell_width//2), (72 + (cell_width//2)) + (cell_width*(y_cells-1)), y_cells)

for image_num in range(num_images):

    lines = np.loadtxt("list.txt", dtype=str, comments="#", delimiter="\n", unpack=False)
    random = np.random.choice(lines, (x_cells * y_cells), replace=False)

    fig = plt.figure(figsize=(14, 14))
    ax = plt.axes(frameon=False, xticks=[], yticks=[])

    n = 0
    for i in range(x_cells):
        for j in range(y_cells):
            lines = text_wrap(random[n], font, cell_width * 0.9)
            for k in range(len(lines)):
                plt.text(x_coords[i], (-len(lines) * line_height/2) + y_coords[j] + k * line_height, lines[k],
                         horizontalalignment='center',
                         verticalalignment='center',
                         clip_on=True,
                         wrap=True,
                         size='xx-large')

            n += 1

    ax.imshow(blank)

    plt.savefig('output_' + str(image_num) + '_.png', bbox_inches='tight', pad_inches=0)

# plt.show()
