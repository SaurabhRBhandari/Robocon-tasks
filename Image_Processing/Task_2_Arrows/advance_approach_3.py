import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

thresh=0.5
# read the image
img = cv2.imread('Arrow_3.jpg',cv2.IMREAD_UNCHANGED)
  
# convert image to gray scale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# detect corners with the goodFeaturesToTrack function.
corners = cv2.goodFeaturesToTrack(gray, 7, 0.01, 10)
corners = np.int0(corners)

# find the center of the arrow
center=np.int0(np.squeeze(np.mean(corners,axis=0)))
x0,y0=center.ravel()

cv2.circle(img,center,3,255,-1)
out=[]
# we iterate through each corner.
for corner in corners:
    x, y = corner.ravel()
    m = (y-y0)/(x-x0)
    c = y-m*x
    dist=[]
    for corner1 in corners:
        x1, y1 = corner1.ravel()
        dist.append(y1-m*x1-c)
    out.append(abs(sum(dist)))

closest_to_zero=min(out)

if closest_to_zero<thresh:
    tip=np.squeeze(corners[out.index(closest_to_zero)])
    x_t,y_t=tip.ravel()
    slope=(y_t-y0)/(x_t-x0)
    print(math.atan(slope)*180/3.14)
    cv2.circle(img,tip,3,255,-1)
    
  
plt.imshow(img), plt.show()