import PIL
from PIL import Image
import pathlib
import math
import matplotlib.pyplot as plt

# Here we load the world map that you need to recreate.
image = Image.open(pathlib.Path('worldmap.jpg'))
image = image.convert('1')
image.thumbnail((400, 400))
image_size = min(image.size)

def get_lidar_reading(centerX, centerY, no_of_rays=360):
    lidar_reading = []

    if image.getpixel((centerX, centerY)) == 0:
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

def plot_reading_on_map(centerX,centerY,map):
    lidar_reading = get_lidar_reading(centerX, centerY)
    if lidar_reading:
        for reading in lidar_reading:
            i = reading[0]
            r = reading[1]
            try:
                x = round(r*math.cos(i*math.pi/180)+centerX)
                y = round(r*math.sin(i*math.pi/180)+centerY)
                map.putpixel((x, y), 255)
                
            except:
                continue

map = PIL.Image.new(mode="1", size=(400, 400))
plt.ion()
for x in range(0,400,10):
    for y in range(0,400,10):
        plot_reading_on_map(x,y,map)
        plt.imshow(map)
        plt.show()
        plt.pause(0.00001)
        plt.clf()

