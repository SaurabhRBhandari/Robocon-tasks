# importing necessary libraries
import numpy as np
from PIL import Image
'''The approach used here is that for every pixel, change the pixel value of all three channels by their average '''
# PIL is used to open the image and then it is converted into a numpy array
image = np.array(Image.open('bees.jpg'))

# The first element of image.shape is the no. of rows and the 2nd element is the no. of columns in the array
for r in range(0, image.shape[0]):
    for c in range(0, image.shape[1]):

        # (r,c) represents one pixel of the image
        # p_r p_g p_b are the pixel values of (r,c)
        p_r, p_g, p_b = image[r, c]

        # g is the pixel value of expected grayscale image,calculated by the average of all three channels
        g = (p_r/3+p_g/3+p_b/3)

        # pixel values of all 3 channels(r,g,b) at (r,c) are set to g
        image[r, c] = (g, g, g)

# The numpy array is converted back to image which is then saved
Image.fromarray(image).save('grayscaled_bees.jpg')
