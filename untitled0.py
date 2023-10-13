# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:49:29 2023

@author: wasi
"""

import numpy, json, random
from tqdm import tqdm
import cv2

# When the intensity doesnt exist in the dictionary.
def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


img = cv2.imread("orignal_image/orignal.jpg", 0)

height, width = img.shape[:2]
# print(height, width)
aspect_ratio = height / width
new_height, new_width = 125, int(125 / aspect_ratio)
# print(new_height, new_width)
img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
xXy = 100

# Creating a blank image to be rendered
final_img = numpy.zeros((new_height * xXy, new_width * xXy), numpy.uint8)


# loading the image based on their intensities.
with open("information.json", "r") as file:
    dict_inten = json.load(file)

inten_lst = list(map(int, list(dict_inten.keys())))
# print(inten_lst)

# acessing each pixel and rendering the image.
for i in tqdm(range(new_height)):
    for j in range(new_width):
        val = img[i][j]
        try:
            temp_img = cv2.imread(
                "grayscale_image/" + random.choice(dict_inten[str(val)]), 0
            )
            final_img[i * xXy : (i + 1) * xXy, j * xXy : (j + 1) * xXy] = temp_img
        except KeyError:
            temp_img = cv2.imread(
                "grayscale_image/"
                + random.choice(dict_inten[str(closest(inten_lst, val))]),
                0,
            )
            final_img[i * xXy : (i + 1) * xXy, j * xXy : (j + 1) * xXy] = temp_img

# writing the final image
cv2.imwrite("f.jpg", final_img)