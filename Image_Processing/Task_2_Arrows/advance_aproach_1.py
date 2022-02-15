# importing necessary libraries
import cv2
import numpy as np
import math

image = cv2.imread('Arrow_1.jpg', cv2.THRESH_BINARY)
image = cv2.blur(image, (6, 6))
corners = cv2.goodFeaturesToTrack(image,5, 0.01, 10)
corners = np.int0(corners).squeeze()
center = np.int0(np.mean(corners, axis=0))
tip = np.zeros_like(center)
print(center)
def angle(a, b, c):
    points = np.array([a, b, c])
    A = points[1] - points[0]
    B = points[2] - points[1]
    C = points[0] - points[2]

    angles = []
    for e1, e2 in ((A, -B), (B, -C), (C, -A)):
        num = np.dot(e1, e2)
        denom = np.linalg.norm(e1) * np.linalg.norm(e2)
        angles.append(np.arccos(num/denom) * 180 / np.pi)
    print(angles)
    print('----------------')
    return(any(angle > 75 and angle < 105 for angle in angles))


for c in corners:
    other_vertices = []
    for o in corners:
        if np.array_equal(o, c):
            continue
        else:
            other_vertices.append(o)
    p1, p2, p3, p4 = other_vertices
    if(angle(p1, p2, p3) and angle(p2, p3, p4) and angle(p3, p4, p1) and angle(p4, p1, p2)):
        tip = c
        break
print(tip)   
slope=(center[1]-tip[1])/(tip[0]-center[0])
if slope>0:
    print (math.atan(slope)*180/3.14)
if slope<0:
    print(180+math.atan(slope)*180/3.14)
if slope==0:
    print(0)