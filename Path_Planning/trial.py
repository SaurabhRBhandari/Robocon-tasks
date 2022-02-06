import tkinter as tk
from MapClass import Map
import time
f = open("map1.txt", "r") # change this location to the location of map1.txt on your device.
dimensions = [int(i) for i in f.readline().split()]
coords = [int(i) for i in f.readline().split()]
array = []
for i in range(dimensions[1]):
    array.append([int(i) for i in f.readline().split()])
map = Map(dimensions[0], dimensions[1], (coords[0],coords[1]), (coords[2],coords[3]), array)
map.add_top_wall(map.end)
current = (map.end[0]-1,map.end[1])
map.add_bottom_wall(current)
print_root = tk.Tk()
print_canvas = tk.Canvas(print_root, bg="white", height=1000+map.height, width=1000+map.width)
print_canvas.pack()
print_canvas.delete("all")
temp = map
print_canvas.create_rectangle((50+(temp.end[1]*50)), (50+(temp.end[0]*50)), (50+((temp.end[1]+1)*50)), (50+((temp.end[0]+1)*50)), fill="#00ff00")
print_canvas.create_rectangle((50+(current[1]*50)), (50+(current[0]*50)), (50+((current[1]+1)*50)), (50+((current[0]+1)*50)), fill="#0000ff")

for i in range(temp.width):
    for j in range(temp.height):
        if temp.check_top_wall((j,i)):
            print_canvas.create_line((50+(i*50)), (50+(j*50)), (50+((i+1)*50)), (50+(j*50)), fill="#000000", width=2)

        if temp.check_left_wall((j,i)):
            print_canvas.create_line((50+(i*50)), (50+(j*50)), (50+(i*50)), (50+((j+1)*50)), fill="#000000", width=2)

        if temp.check_right_wall((j,i)):
            print_canvas.create_line((50+((i+1)*50)), (50+(j*50)), (50+((i+1)*50)), (50+((j+1)*50)), fill="#000000", width=2)

        if temp.check_right_wall((j,i)):
            print_canvas.create_line((50+(i*50)), (50+((j+1)*50)), (50+((i+1)*50)), (50+((j+1)*50)), fill="#000000", width=2)

print_canvas.update()
print(map.array)
time.sleep(5)
print(current)
print(map.end)
print(map.check_top_wall(map.end))
print(map.check_bottom_wall(current))