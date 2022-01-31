# importing necessary libraries
import numpy as np
from PIL import Image

#defines the intensity of blur required to be achieved
level =10

'''The approach used here is that for every pixel, change the pixel value of each channel to the average of pixel values of all its neigbourhood points '''

# PIL is used to open the image and then it is converted into a numpy array
image = np.array(Image.open('hills.jpg'))

def blur(image):
    '''Blurs the image by one level'''
    blurred_image=np.empty(image.shape)

    # The first element of image.shape is the no. of rows and the 2nd element is the no. of columns in the array
    for r in range(0, image.shape[0]):
        for c in range(0, image.shape[1]):
            
            #stores all the points in the neighbourhood of (r,c) pixel
            nbd=image[r-1:r+2,c-1:c+2]

            #avg_p stores the average pixel value in (r,g,b) format
            avg_p=np.mean(nbd,axis=(0,1),dtype=np.uint16)
            
            #the pixel of (r,c) pixel is set to the average_p
            blurred_image[r,c]=avg_p

    
    # The numpy array is converted back to image which is then saved
    return(blurred_image)

#call the functions 'level' times to achieve blurring of that many levels
for i in range(0,level):
    image=blur(image)

#Converts the image to -ve as it is going to be again inverted in the next step
image=256-image

# The numpy array is converted back to image which is then saved
Image.fromarray((image * 255).astype(np.uint8)).save('blurred_hills.jpg')
#asstype is used here as the program was giving an error which may be due to PIL not accepting RGB values in the float (0,1) format :)        