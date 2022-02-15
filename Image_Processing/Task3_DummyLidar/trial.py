import PIL
from PIL import Image,ImageDraw
import pathlib
import math
import matplotlib.pyplot as plt
from PIL import ImageFilter





'''This program is just to check if the points given by dummylidar.py program are physically viable in real world scenario in the order they are,
refer to dummylidar.py for the actual algorithm'''







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
    print(f'{centerX},{centerY}')    
    for i,reading in enumerate(lidar_reading):
            try:
                i0=reading[0]
                r0=reading[1]
                i1=lidar_reading[i+1][0]
                r1=lidar_reading[i+1][1]
                x0 = int(r0*math.cos(i0*math.pi/180)+centerX)
                y0 = int((r0*math.sin(i0*math.pi/180)+centerY))
                
                x1 = int(r1*math.cos(i1*math.pi/180)+centerX)
                y1 = int((r1*math.sin(i1*math.pi/180)+centerY))
                draw=ImageDraw.Draw(map)
                draw.polygon([(centerX,centerY),(x0,y0),(x1,y1)], fill =255, outline =255)
                
            except:
                continue

map = PIL.Image.new(mode="1", size=(400, 400))
plt.ion()
plot_reading_on_map(0,320,map)
#map = map.filter(ImageFilter.MedianFilter(size = 11)) 
plt.imshow(map)
plt.show()
plt.pause(5)
plt.clf()


plot_reading_on_map(80,140,map)
#map = map.filter(ImageFilter.MedianFilter(size = 11))
plt.imshow(map)
plt.show()
plt.pause(5)
plt.clf()


plot_reading_on_map(200,0,map)
#map = map.filter(ImageFilter.MedianFilter(size = 11))
plt.imshow(map)
plt.show()
plt.pause(5)
plt.clf()


plot_reading_on_map(200,280,map)
#map = map.filter(ImageFilter.MedianFilter(size = 11))
plt.imshow(map)
plt.show()
plt.pause(5)
plt.clf()


plot_reading_on_map(280,260,map)
#map = map.filter(ImageFilter.MedianFilter(size = 11))
plt.imshow(map)
plt.show()
plt.pause(5)
plt.clf()