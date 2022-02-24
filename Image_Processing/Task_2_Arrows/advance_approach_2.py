import numpy as np
import cv2


def center_arrow(image):
    '''
    Crops the image to remove unnecesarry portion. This is done to-
        1.Reduce the computational time
        2.Center the arrow
    '''
    # get the points inside the arrow
    x, y = np.where(image == 1)

    # get the rectangular bounds of arrow
    xmin = np.min(x)
    xmax = np.max(x)
    ymin = np.min(y)
    ymax = np.max(y)

    # store the height and breadth
    a = xmax-xmin
    b = ymax-ymin

    # if width>height, increase height
    if(a >= b):
        lb_y = ymin-int((a-b)/2)
        lb_x = xmin
        ru_y = ymax+int((a-b)/2)
        ru_x = xmax

    # if height>width, increase breadth
    else:
        lb_x = xmin-int((b-a)/2)
        lb_y = ymin
        ru_x = xmax+int((b-a)/2)
        ru_y = ymax

    centered_image = image[lb_x-20:ru_x+20, lb_y-20:ru_y+20]

    # return a cropped,squared,centered image of the arrow
    return centered_image


def change_angle_to_radius_unit(angle):
    angle_radius = angle * (np.pi/180)
    return angle_radius


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


class BasicOrientation:

    def __init__(self, image):
        '''Initializing the parameters of our detector'''

        # The original image of arrow
        self.image = image

        # get the X-flip and Y-flip of image
        self.X_flip, self.Y_flip = self.get_flipped_images()

        # find the match of image with it's X-flip and Y-flip
        self.match_X = np.where(
            self.image == 255, (self.image == self.X_flip), 0).astype('uint8')*255
        self.match_Y = np.where(
            self.image == 255, (self.image == self.Y_flip), 0).astype('uint8')*255

    def center_arrow(self):
        '''
        Crops the image to remove unnecesarry portion. This is done to-
            1.Reduce the computational time
            2.Center the arrow
        '''
        # get the points inside the arrow
        x, y = np.where(self.image == 1)

        # get the rectangular bounds of arrow
        xmin = np.min(x)
        xmax = np.max(x)
        ymin = np.min(y)
        ymax = np.max(y)

        # store the height and breadth
        a = xmax-xmin
        b = ymax-ymin

        # if width>height, increase height
        if(a >= b):
            lb_y = ymin-int((a-b)/2)
            lb_x = xmin
            ru_y = ymax+int((a-b)/2)
            ru_x = xmax

        # if height>width, increase breadth
        else:
            lb_x = xmin-int((b-a)/2)
            lb_y = ymin
            ru_x = xmax+int((b-a)/2)
            ru_y = ymax

        centered_image = self.image[lb_x-20:ru_x+20, lb_y-20:ru_y+20]

        # return a cropped,squared,centered image of the arrow
        return centered_image

    def get_flipped_images(self):
        '''Flips the image about X and Y axis and returns the two flipped image'''

        image_flipped_X = np.flipud(self.image)  # flipping image about X
        image_flipped_Y = np.fliplr(self.image)  # flipping image about Y

        return image_flipped_X, image_flipped_Y
    
    def get_match(self):
        # number of pixels matching between image and it's X-flip
        x = np.count_nonzero(self.match_X)
        # number of pixels matching between image and it's Y-flip
        y = np.count_nonzero(self.match_Y)

        self.match_x = x/np.count_nonzero(self.image)
        self.match_y = y/np.count_nonzero(self.image)
        
        
   
    def get(self):
        '''Returns the orientation of arrow x+,x-,y+,y-'''

        # get the points inside the arrow
        X, Y = np.where(self.image == 255)
        h, w = self.image.shape

        # if image matches with it's X-flip
        if self.match_x > self.match_y:

            for i, y in np.ndenumerate(Y):

                if np.count_nonzero((self.image[int(h/2)-5:int(h/2)+5, y])) < 4:
                    break

            # stores the coords of tip of arrow with origin at arrow's centre
            tip = np.array((X[i], Y[i]))-np.array(self.image.shape)/2

            if tip[1] < 0:
                return('x-')

            if tip[1] > 0:
                return('x+')

        # if image matches with it's Y-flip
        if self.match_y > self.match_x:

            for i, x in np.ndenumerate(X):

                if np.count_nonzero((self.image[x, int(w/2)-5:int(w/2)+5])) < 4:
                    break

            # stores the coords of tip of arrow with origin at arrow's centre
            tip = np.array((X[i], Y[i]))-np.array(self.image.shape)/2

            if tip[0] < 0:
                return('y+')

            if tip[0] > 0:
                return('y-')
            


# make an object of the image of arrow
image = cv2.imread('Arrow_1.jpg', cv2.THRESH_BINARY)

# pre-processing the image
image = center_arrow(image)
image[image < 50] = 0
image[image > 50] = 255
center = np.int0(np.array(image.shape)/2)
#cv2.imshow('image', image)
#cv2.imshow('rotated_image', cv2.medianBlur(
#    rotate(image, 90, center, image.shape), 3))
#cv2.waitKey(0)
#cv2.destroyAllWindows()
orientation = None
matches_X=[]
matches_Y=[]
for i in range(0,361):
    image_rotated = cv2.medianBlur(rotate(image, i, center, image.shape), 3)
    ori = BasicOrientation(image_rotated)
    ori.get_match()
    matches_X.append(ori.match_x)
    matches_Y.append(ori.match_y)
    
print(matches_X.index(max(matches_X)))
print(matches_Y.index(max(matches_Y)))
