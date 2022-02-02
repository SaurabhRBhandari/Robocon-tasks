import PIL
from PIL import Image, ImageDraw
import pathlib
import math

# Here we load the world map that you need to recreate.
image = Image.open(pathlib.Path('worldmap.jpg'))
image = image.convert('1')
image.thumbnail((400, 400))
image_size = min(image.size)

# This stores the map created by lidar
map = PIL.Image.new(mode="1", size=image.size)


def get_lidar_reading(centerX, centerY, no_of_rays=360):
    '''This mimics the lidar sensor'''

    lidar_reading = []

    if image.getpixel((centerX, centerY)) == 0:
        # This just would'nt work in real life
        pass
    else:
        for i in range(0, 360, int(360/no_of_rays)):
            r = 0

            currentX = round(centerX + r*math.cos(i*math.pi/180))
            currentY = round(centerY + r*math.sin(i*math.pi/180))

            while ((currentX < image_size and currentX >= 0) and (currentY < image_size and currentY >= 0) and (image.getpixel((currentX, currentY)) != 0)):
                currentX = round(centerX + r*math.cos(i*math.pi/180))
                currentY = round(centerY + r*math.sin(i*math.pi/180))
                r += 1

            lidar_reading.append((i, r))

        return lidar_reading


def plot_reading_on_map(centerX, centerY, lidar_reading, map):
    '''This plots the collected lidar data on map'''
    for i, reading in enumerate(lidar_reading):

        try:
            '''As the angle given by lidar is integral,
            if we try to map all the points where lidar's light could pass,
            we see that the generated map doesnt show the points between two light rays.
            So here I have collected two consecutive points which lidar has detected,which are
            expected to be at a very close distance,and then collect all the points inside the
            triangle formed by these points-
            1.point where the sensor is
            2 and 3.The close consecutive points
            Credits-MATH calculus course :)
            '''
            i0 = reading[0]
            r0 = reading[1]

            i1 = lidar_reading[i+1][0]
            r1 = lidar_reading[i+1][1]

            x0 = int(r0*math.cos(i0*math.pi/180)+centerX)
            y0 = int((r0*math.sin(i0*math.pi/180)+centerY))

            x1 = int(r1*math.cos(i1*math.pi/180)+centerX)
            y1 = int((r1*math.sin(i1*math.pi/180)+centerY))

            draw = ImageDraw.Draw(map)
            draw.polygon([(centerX, centerY), (x0, y0),
                         (x1, y1)], fill=255, outline=255)

        except:
            # to avoid encountering error at the edges
            continue


for x in range(0, image_size, int(image_size/20)):
    for y in range(0, image_size, int(image_size/20)):

        if(map.getpixel((x, y)) == 0):  # If a point is already seen by the lidar,it is skipped
            
            # Lidar won't necesarilly work for all points,it would skip the black spaces in real world
            lidar_reading = get_lidar_reading(x, y)
            
            if lidar_reading:
                
                # These are the points where lidar will actually work
                print(f'({x},{y})')
                plot_reading_on_map(x, y, lidar_reading, map)


#Finally saving the map created
map.save('map.jpg')