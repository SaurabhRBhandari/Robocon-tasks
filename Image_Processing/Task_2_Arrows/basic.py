from re import X
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
    X,Y=np.where(image==255)
    if x>y:
        for i,y in np.ndenumerate(Y):
            if np.count_nonzero((image[:,y]))<4:
                break
        tip=np.array((X[i],Y[i]))-np.array(image.shape)/2
        if tip[1]<0:
            return('x-')
        if tip[1]>0:
            return('x+')
    if y>x:
        for i,x in np.ndenumerate(X):
            if np.count_nonzero((image[x,:]))<4:
                break
        tip=np.array((X[i],Y[i]))-np.array(image.shape)/2
        if tip[0]<0:
            return('y+')
        if tip[0]>0:
            return('y-')

#def get_tip(image):
#    for i,x in np.ndenumerate(X):
#        if np.count_nonzero((image[x,:]))<3:
#            break
#   print(X[i],Y[i])
    
image = cv2.imread('Arrow_2.jpg', cv2.THRESH_BINARY)
image = center_arrow(image)
image[image<50]=0
image[image>50]=255
X_flip,Y_flip=get_flipped_images(image)
match_X=np.where(image==255,(image==X_flip),0).astype('uint8')*255
match_Y=np.where(image==255,(image==Y_flip),0).astype('uint8')*255
print(find_orientation(match_X,match_Y,image))
cv2.imshow('image',image)
cv2.imshow('X',match_X)
cv2.imshow('Y',match_Y)
cv2.waitKey(0)
cv2.destroyAllWindows()
