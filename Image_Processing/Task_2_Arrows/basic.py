# importing necesarry libraries
import cv2
import numpy as np

'''
The approach used here is to find the axis and tip of arrow to comment on it's orientation.
For the axis we flip the image about X and Y and check which is identical to original image.
For the tip, we check pixels near axis 
'''


class BasicOrientation:
    def __init__(self, image):
        self.image = image

        # pre-processing the image
        self.image = self.center_arrow()
        self.image[self.image < 50] = 0
        self.image[self.image > 50] = 255

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

    def get(self):
        '''Returns the orientation of arrow x+,x-,y+,y-'''

        # number of pixels matching between image and it's X-flip
        x = np.count_nonzero(self.match_X)
        # number of pixels matching between image and it's Y-flip
        y = np.count_nonzero(self.match_Y)

        # get the points inside the arrow
        X, Y = np.where(self.image == 255)
        h, w = self.image.shape

        # if image matches with it's X-flip
        if x > y:

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
        if y > x:

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
image = cv2.imread('Arrow_2.jpg', cv2.THRESH_BINARY)

image_ori=BasicOrientation(image)
print(image_ori.get())

