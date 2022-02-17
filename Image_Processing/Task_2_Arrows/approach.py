
import numpy as np
import cv2


def change_angle_to_radius_unit(angle):
    angle_radius = angle * (np.pi/180)
    return angle_radius


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


image = cv2.imread('Arrow_3.jpg', cv2.THRESH_BINARY)
x, y = np.where(image == 1)


lb_y, lb_x, ru_y, ru_x = get_squared_dimensions(x, y)
image = image[lb_x-20:ru_x+20, lb_y-20:ru_y+20]
height, width = image.shape[:2]


def get_points(x, y):
    points = np.zeros(shape=(x.size, 2), dtype=np.uint16)
    for i in range(0, x.size):
        points[i][0] = x[i]
        points[i][1] = y[i]
    return(points)


def rotate(src_img, angle_of_rotation, pivot_point, shape_img):

    # 1.create rotation matrix with numpy array
    rotation_mat = np.transpose(np.array([[np.cos(angle_of_rotation), -np.sin(angle_of_rotation)],
                                          [np.sin(angle_of_rotation), np.cos(angle_of_rotation)]]))
    h, w = shape_img

    pivot_point_x = pivot_point[0]
    pivot_point_y = pivot_point[1]

    new_img = np.zeros(src_img.shape, dtype='u1')

    for height in range(h):  # h = number of row
        for width in range(w):  # w = number of col
            xy_mat = np.array([[width-pivot_point_x], [height-pivot_point_y]])

            rotate_mat = np.dot(rotation_mat, xy_mat)

            new_x = pivot_point_x + int(rotate_mat[0])
            new_y = pivot_point_y + int(rotate_mat[1])

            if (0 <= new_x <= w-1) and (0 <= new_y <= h-1):
                new_img[new_y, new_x] = src_img[height, width]

    return new_img


x, y = np.where(image == 1)
points = get_points(x, y)
center = np.mean(points, axis=0, dtype=np.uint16)

own_rotated = rotate(image.copy(), change_angle_to_radius_unit(
    -45), center, (height, width))
own_rotated = cv2.medianBlur(own_rotated, 3)


cv2.imshow('image', image)
cv2.imshow('rotated image', own_rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
