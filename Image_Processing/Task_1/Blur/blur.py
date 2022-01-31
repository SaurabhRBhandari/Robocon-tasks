# importing necessary libraries
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
intensity =5

'''The approach used here is that for every pixel, change the pixel value of all three channels by their average '''
# PIL is used to open the image and then it is converted into a numpy array
image = np.array(Image.open('hills.jpg').convert('RGB'))
blurred_image=np.empty(image.shape)

# The first element of image.shape is the no. of rows and the 2nd element is the no. of columns in the array
for r in range(0, image.shape[0]):
    for c in range(0, image.shape[1]):
        #stores all the points in the neighbourhood of (r,c)
        nbd=image[r-1:r+2,c-1:c+2]
        
        #acg_p stores the average pixel value in (r,g,b) format
        avg_p=np.mean(nbd,axis=(0,1),dtype=np.uint16)
        blurred_image[r,c]=tuple(avg_p)
        
blurred_image=256-blurred_image
# The numpy array is converted back to image which is then saved
Image.fromarray((blurred_image * 255).astype(np.uint8)).save('blurred_hills.jpg')



        