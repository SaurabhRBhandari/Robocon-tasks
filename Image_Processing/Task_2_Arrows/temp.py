import cv2
import numpy as np
image=cv2.imread('arrow.jpg')
image=image[:-10][:-10]
cv2.imwrite('Arrow_4.jpg',~image)