import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

#if the value of slope falls out of these, consider the arrow to be aligned to the axis
m_min=0.017455
m_max=57.289

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

tip=None

# we iterate through each corner.
for p in corners:
       
    #get the co-ordintaes of P
    x, y = p.ravel()
    
    #make a line L passing through center and point p
    m = (y-y0)/(x-x0)
    if abs(m)<m_min or abs(m)>m_max:
        tip=p
        break
    
    c = y0-m*x0
    
    dist=0
    
    for q in corners:
        
        #get the coordinates of Q
        x1, y1 = q.ravel()
        
        #skip if P and Q are same points
        if x1==x and y1==y:
            continue
        
        #put the point Q in equation of line L
        dist+=y1-m*x1-c
    
    #closer this is to 0, more does L represent the line of symmetry
    out.append(abs(dist))
    
#find the closest_to_zero term in out and the point it corresponds to


if tip is None:
    closest_to_zero=min(out)
    tip=corners[out.index(closest_to_zero)]

#extract the coordintaes of tip
x_t,y_t=np.squeeze(tip.ravel())
dy=y_t-y0
dx=x_t-x0
angle=math.atan(dy/dx)*180/np.pi

# I realized that the (x,y) we generakky use is'nt the way image has it's coordinate system,so we have to do some operations
# (I could'nt give this step enough time,so may be prone to some errors,so i have also marked the tip and cetre in image)

if dy<0 and dx<0:
    angle=180-angle

elif abs(dx)<2:
    angle*=-1

elif abs(dy)<2:
    if dx>0:
        angle=0
    else:
        angle=180        

print(dy,dx,angle)
cv2.circle(img,(x_t,y_t),3,255,-1)
    
plt.imshow(img)
plt.show()  
