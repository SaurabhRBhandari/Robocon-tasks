# importing necessary libraries

import numpy as np
from PIL import Image

Gx = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]
])

Gy = np.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1]
])

'''The approach used here is that for every pixel, we calculate the derivative of pixel value
in both x and y directions using sobel's method,denoted by gx and gy.The overall change is then
calculated using sqrt(gx^2+gy^2).This change should have a hogh value at the edge'''

# PIL is used to open the image and then it is converted into a numpy array
image = np.array(Image.open('flower.jpg').convert("L"))

# A template for storing the resultant image
edged_image = np.zeros_like(image)


# The first element of image.shape is the no. of rows and the 2nd element is the no. of columns in the array
for r in range(0, image.shape[0]-3):
    for c in range(0, image.shape[1]-3):
        
        #A small part of image(variable name inspired by work-peice ~as i was doing this while attending WS lecture~ :) )
        peice = image[r:r+3, c:c+3]
        
        
        gx = np.sum(np.multiply(Gx, image[r:r + 3, c:c + 3]))  # x direction
        gy = np.sum(np.multiply(Gy, image[r:r + 3, c:c + 3]))  # y direction
        g = np.sqrt(gx**2+gy**2)  # the overall change
        
        #Assigning the pixel value to the derivative,because it would be high if there's an edge,and low otherwise
        edged_image[r+1, c+1] = g


# The numpy array is converted back to image which is then saved
Image.fromarray(edged_image).save('edged_flower.jpg')
