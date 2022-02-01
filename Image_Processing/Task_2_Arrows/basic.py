# importing necessary libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
sys.path.append("..")
from Task_1.Edge.edge import edge

image = cv2.imread('Arrow_1.jpg', cv2.THRESH_BINARY)
image_edge=np.array(edge(image))
def get_points(x,y):
    points=np.zeros(shape=(x.size,2),dtype=np.uint16)
    for i in range(0,x.size):
        points[i][0]=x[i]
        points[i][1]=y[i]
    return(points)

def get_center_points(points):
    return np.mean(points,axis=0)

x,y=np.where(image == 1)
points=get_points(x,y)
x,y=np.where(image_edge == 1)
edge_points=get_points(x,y)
center_1=np.mean(points,axis=0)

center_2=np.median(points,axis=0)

center_3=np.mean(edge_points,axis=0)

center_4=np.median(edge_points,axis=0)

slope,b=np.polyfit([
                  center_1[0],
                  center_2[0],
                  center_3[0],
                  center_4[0],
                  ],
               [
                  center_1[1],
                  center_2[1],
                  center_3[1],
                  center_4[1],
                  ],
               1
               )
print(slope)