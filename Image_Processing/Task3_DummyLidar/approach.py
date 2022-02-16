import random
import PIL
from PIL import Image, ImageDraw
import pathlib
import math
import numpy as np
import matplotlib.pyplot as plt
# Getting correct output for world map motivated me to try this out on a more complex map,so i have also tested it on world map 2 downloaded from internet.
# To be honest it did work properly but there was only a small distortion (see the map2quality=20.jpg)
# So I have included quality factor in the code,increasing it would increase the quality of map at the cost of more points being needed
# quality is to be set based on a rough estimate about the complexity of map

image = Image.open(pathlib.Path('worldmap.jpg'))
image = image.convert('1')
image.thumbnail((400, 400))
image_size = min(image.size)


def get_lidar_reading(centerX, centerY, no_of_rays=360):
    '''This mimics the lidar sensor'''

    lidar_reading = []

    if image.getpixel((centerX, centerY)) == 0:
        print("invalid")
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


'''
Workflow-
1.Consider only some points(number is determined by the quality of map seeked for)
2.If the point is already detected,remove it from schrodingers points
3.If the point is known to be inside a wall fs, remove it from schrodingers points
4.The next scan must be on a detected point.
5.To decide scan,make a hill at every scanned point and then find the place of lowest height.
6.. Repeat until we dont have any scrodingers point left
'''
# TODO: correct is_inside_wall function
# TODO: make get_scan function


class LidarScanner:
    def __init__(self, initialX, initialY, map_size, quality1=20, quality2=1):
        self.position = [initialX, initialY]
        self.map = map = PIL.Image.new(mode="1", size=map_size)
        self.map_quality = quality1
        self.schr_points = []
        self.schr_negligence = quality2
        self.detected_points = [(initialX, initialY)]
        self.scanned_points=[]
        self.walls = []
        for (x, y), point in np.ndenumerate(np.zeros_like(map)):
            if x % quality1 == 0 and y % quality1 == 0:
                self.schr_points.append((x, y))

    def run_scanner(self):
        first_run=True
        while len(self.schr_points) >= self.schr_negligence:
            for point in self.schr_points:
                self.is_detected(point)
                #self.is_inside_wall(point)
            scan_point = self.get_next_scan()
            print(scan_point)
            self.position = scan_point
            print(self.position)
            lidar_reading = get_lidar_reading(
                self.position[0], self.position[1])
            self.plot_reading_on__map(lidar_reading)
            self.display_map()
            self.scanned_points.append(scan_point)
            print(len(self.schr_points))

    def is_detected(self, point):
        if self.map.getpixel(point) != 0:
            self.schr_points.remove(point)
            self.detected_points.append(point)
            return True
        else:
            return False

    def is_inside_wall(self, point):
        cnt = 0
        edge = 0
        if self.map.getpixel(point) == 0:
            for x in range(point[0], self.map.size[0]):
                if self.map.getpixel((x, point[1])) != 0:
                    cnt += 1
                    break
                if x == self.map.size[0]-1:
                    edge += 1
                    break
            for x in range(point[0]):
                if self.map.getpixel((x, point[1])) != 0:
                    cnt += 1
                    break
                if x == 0:
                    edge += 1
                    break
            for y in range(point[1], self.map.size[1]):
                if self.map.getpixel((point[0], y)) != 0:
                    cnt += 1
                    break
                if y == self.map.size[1]-1:
                    edge += 1
                    break
            for x in range(point[1]):
                if self.map.getpixel((point[0], y)) != 0:
                    cnt += 1
                    break
                if y == 0:
                    edge += 1
                    break
            if point == (0, 0):
                edge = 2
            print(cnt, edge)
            if cnt+edge <= 4 and cnt+edge >= 3:
                self.schr_points.remove(point)
                return True

    def get_next_scan(self):
        dist = {}
        for point in self.detected_points:
            d=[]
            if point not in self.scanned_points:
                for pt in self.scanned_points:
                    distance=(point[0]-pt[0])**2+(point[1]-pt[1])**2
                    if distance>10000:
                        d.append(distance)
                    else:
                        break
                dist[point]=sum(d)
        
        v = list(dist.values())
 
        
        k = list(dist.keys())
        
        return(k[v.index(max(v))])

    def plot_reading_on__map(self, lidar_reading):
        '''This plots the collected lidar data on map'''
        centerX = self.position[0]
        centerY = self.position[1]
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

                self.walls.append((x0, y0))

                draw = ImageDraw.Draw(self.map)
                draw.polygon([(centerX, centerY), (x0, y0),
                              (x1, y1)], fill=255, outline=255)

            except:
                # to avoid encountering error at the edges
                continue

    def display_map(self):
        plt.imshow(self.map, cmap='gray')
        plt.show()
    
    def get_distance(self,point):
        return (self.position[0]-point[0])**2+(self.position[1]-point[1])**2

ls = LidarScanner(initialX=399, initialY=0, map_size=image.size)
ls.run_scanner()
ls.display_map()
