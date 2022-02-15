import cv2
import numpy as np


def center_arrow(image):
    x, y = np.where(image == 1)
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
    else:
        lb_x = xmin-int((b-a)/2)
        lb_y = ymin
        ru_x = xmax+int((b-a)/2)
        ru_y = ymax

    centered_image = image[lb_x-20:ru_x+20, lb_y-20:ru_y+20]
    return centered_image

def get_flipped_images(image):
    image_flipped_X=np.flipud(image)
    image_flipped_Y=np.fliplr(image)
    return image_flipped_X,image_flipped_Y
    
def find_orientation(match_X,match_Y,image):
    x=np.count_nonzero(match_X)
    y=np.count_nonzero(match_Y)
    print(x,y)
    X,Y=np.where(image!=0)
    if x>y:
        return('x')
    if y>x:
        return('y')
    
image = cv2.imread('Arrow_4.jpg', cv2.THRESH_BINARY)
cv2.imshow('image',image)
image = center_arrow(image)
X_flip,Y_flip=get_flipped_images(image)
match_X=np.where(image==255,(image==X_flip),0).astype('uint8')*255
match_Y=np.where(image==255,(image==Y_flip),0).astype('uint8')*255
print(find_orientation(match_X,match_Y,image))
cv2.imshow('X',match_X)
cv2.imshow('Y',match_Y)
cv2.waitKey(0)
cv2.destroyAllWindows()
