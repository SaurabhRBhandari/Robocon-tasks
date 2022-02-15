from cv2 import blur
import numpy as np
import cv2


def get_squared_dimensions(x, y):
    xmin = np.min(x)
    xmax = np.max(x)
    ymin = np.min(y)
    ymax = np.max(y)
    a = xmax-xmin
    b = ymax-ymin
    if(a >= b):
        lb_y = ymin-int((a-b)/2)
        lb_x = xmin
        ru_y = ymax+int((a-b)/2)
        ru_x = xmax

        return lb_y, lb_x, ru_y, ru_x
    else:
        lb_x = xmin-int((b-a)/2)
        lb_y = ymin
        ru_x = xmax+int((b-a)/2)
        ru_y = ymax

        return lb_y, lb_x, ru_y, ru_x


def get_points(x, y):
    points = np.zeros(shape=(x.size, 2), dtype=np.uint16)
    for i in range(0, x.size):
        points[i][0] = x[i]
        points[i][1] = y[i]
    return(points)


image = cv2.imread('Arrow_2.jpg', cv2.THRESH_BINARY)
x, y = np.where(image == 1)

# Cropping the image to center the arrow
lb_y, lb_x, ru_y, ru_x = get_squared_dimensions(x, y)
image = image[lb_x-20:ru_x+20, lb_y-20:ru_y+20]
height, width = image.shape[:2]


#x_all, y_all = np.where(image == 1)
#points = get_points(x, y)
#center = np.mean(points, axis=0, dtype=np.uint16)
image_flipped_X=np.flipud(image)
image_flipped_Y=np.fliplr(image)
#print(dist)
matchX=(image==image_flipped_X)
matchY=(image==image_flipped_Y)

#print(np.average(matchY))
cv2.imshow('imageX', image_flipped_X)
cv2.imshow('imageY', image_flipped_Y)
cv2.imshow('image',image)
#cv2.imshow('matchesX')
#cv2.imshow('matchesY',matchY)
cv2.waitKey(0)
cv2.destroyAllWindows()
