import cv2
from skimage.metrics import structural_similarity as ssim
import glob
import numpy as np
import csv
import os
# import matplotlib.pyplot as plt
from sewar.full_ref import mse


def get_closest_match(test_image_path, database):

    test_image = cv2.imread(test_image_path)

    x, y = get_cross_location(test_image)
    crop = crop_around_cross(test_image, x, y)

    test_image = resize_image(crop)

    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

    # plt.figure()
    # plt.imshow(test_image)
    # plt.show()

    if database == "":
        possible_images = glob.glob("resources/images/maps/" + "sb" + "/*.png")\
                          + glob.glob("resources/images/maps/" + "shb" + "/*.png")\
                          + glob.glob("resources/images/maps/" + "ew" + "/*.png")
    else:
        possible_images = glob.glob("resources/images/maps/" + database + "/*.png")

    max_sim = 99999999999999999999
    best_image_path = ""

    for image in possible_images:
        im = cv2.imread(image)
        im = resize_image(im)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # sim = ssim(im, test_image, data_range=255)
        sim = mse(im, test_image)

        if sim < max_sim:
            max_sim = sim
            best_image_path = image

    # print("similarity: " + str(max_sim))
    coords = get_coords(os.path.basename(best_image_path)[:-4])

    return best_image_path, coords


def resize_image(image, size=100):
    resized_image = cv2.resize(image, (size, size))
    return resized_image


def get_cross_location(image):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([5, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170, 70, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0 + mask1

    # plt.figure()
    # plt.imshow(mask)

    center = [np.average(indices) for indices in np.where(mask >= 255)]
    center = list(map(int, center))
    return center


def crop_around_cross(image, center_x, center_y, size=70):

    cropped_image = image[(center_x - size):(center_x + size), (center_y - size):(center_y + size)]
    return cropped_image


def get_coords(filename):
    with open("resources/images/maps/coordinates.csv", "r") as csv_file:
        coordinates = csv.reader(csv_file, delimiter=',')
        for row in coordinates:
            if filename == row[0]:
                print(row[1:])
                return row[1:]

# test = cv2.imread(r"C:\Users\ttocs\PycharmProjects\FF Bingo\resources\images\maps\test.png")
#
# get_closest_match(test, "shb")
#
# plt.show()

