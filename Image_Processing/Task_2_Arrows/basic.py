# importing necessary libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('Arrow_2.jpg', cv2.THRESH_BINARY)
print(image)
#x,y = np.where(image == 1)
#u_x=list(dict.fromkeys(x))
#def width(x0,x):
#    w = 0
#    print(f'----{x0}----')
#    for i in range (0,len(x)):
#            if(x[i]==x0):
#                w+=1
#    return(w)

#for i in range(0,len(u_x)):
#    count = (x == u_x[i]).sum()
#    print(f'{u_x[i]}-->{count}')
