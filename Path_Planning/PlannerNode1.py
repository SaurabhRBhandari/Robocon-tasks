# Importing necessary libraries
import random
import math
import numpy as np
import time

from MapNode import MapNode

import tkinter

class PlannerNode:

    def __init__(self):
        '''Initializes the attribute of PlannerNode'''

        self.current_obj = MapNode()
        self.path_taken=[]
        self.path_taken.append(self.current_obj.current)
        
        # Since we know that the first step the bot will take will be down, we can simply do it here
        #self.current_obj.direction_callback("down")  # example 1
        #self.path_taken.append(self.current_obj.current)
        
        self.wall_callback()  # start exploring the maze

    def wall_callback(self):
    

        # till the bot reaches the end
        while self.current_obj.current != self.current_obj.walls.end:
            self.path_taken.append(self.current_obj.current)
            start=self.current_obj.current
            path=self.astar(start)
            self.take_step(path[1])
            #time.sleep(2)
            if len(self.path_taken)<20:    
                self.show_path(path)
            

    def astar(self,start):
        old_path= self.path_taken
        old_path.append(start)
        end=self.current_obj.walls.end
        
        a=np.zeros((self.current_obj.walls.height,self.current_obj.walls.width),dtype=np.uint32)
        m=np.zeros_like(a)
        m[start[0]][start[1]]=1
        
        k=0
        
        while m[end[0]][end[1]]==0:
            k+=1
            
            for i in range(len(m)):
                for j in range(len(m[i])):
                    walls=self.current_obj.walls
                    
                    if m[i][j]==k:
                        
                        if i>0 and m[i-1][j]==0 and a[i-1][j]==0:
                            if (i,j) in old_path and walls.check_top_wall((i,j)):
                                continue
                            else:
                               m[i-1][j]=k+1
                               
                        if j>0 and m[i][j-1]==0 and a[i][j-1]==0:
                            if (i,j) in old_path and walls.check_left_wall((i,j)):
                                continue
                            else:
                               m[i][j-1]=k+1
                        
                        if i < len(m)-1 and m[i+1][j] == 0 and a[i+1][j] == 0:
                            if (i,j) in old_path and walls.check_bottom_wall((i,j)):
                                continue
                            else:
                                m[i+1][j] = k + 1

                        if j < len(m[i])-1 and m[i][j+1] == 0 and a[i][j+1] == 0:
                            if (i,j) in old_path and walls.check_right_wall((i,j)):
                                continue
                            else:
                               m[i][j+1] = k + 1
            # start from the end point
        i, j = end

        # the value of end point in m
        k = m[i][j]

        # store the path here,(reversed)
        path = [(i, j)]

        # till we reach the start again
        while k > 1:

            # find a neighbour cell with value k-1, go there decrease k by 1.

            if i > 0 and m[i - 1][j] == k-1:
                i, j = i-1, j
                path.append((i, j))
                k -= 1

            elif j > 0 and m[i][j - 1] == k-1:
                i, j = i, j-1
                path.append((i, j))
                k -= 1

            elif i < len(m) - 1 and m[i + 1][j] == k-1:
                i, j = i+1, j
                path.append((i, j))
                k -= 1

            elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
                i, j = i, j+1
                path.append((i, j))
                k -= 1

        # the path is from end-point to start-point so reverse it.
        path.reverse()

        # return the path calculated
        return path
                                
                                
                    
    def take_step(self,final_pos):
        x0,y0=self.current_obj.current
        x1,y1=final_pos
        if y1-y0<0:
            print("left")
            self.current_obj.direction_callback("left")
        if y1-y0>0:
            print("right")
            self.current_obj.direction_callback("right")
        if x1-x0>0:
            print("down")
            self.current_obj.direction_callback("down")
        if x1-x0<0:
            print("up")
            self.current_obj.direction_callback("up")
    
    
                    
    def show_path(self, path):
        '''Displays the shortest path decide by the bot'''

        width = self.current_obj.walls.width
        height = self.current_obj.walls.height
        print_root = tkinter.Tk()
        print_canvas = tkinter.Canvas(
            print_root, bg="white", height=50+height*50, width=50+width*50)
        end = self.current_obj.walls.end
        start = self.current_obj.walls.start
        print_canvas.create_rectangle(
            (50+(end[1]*50)), (50+(end[0]*50)), (50+((end[1]+1)*50)), (50+((end[0]+1)*50)), fill="#0000ff")
        print_canvas.create_rectangle((50+(start[1]*50)), (50+(start[0]*50)), (50+(
            (start[1]+1)*50)), (50+((start[0]+1)*50)), fill="#000000")
        for step in path:
            if step == end or step == start:
                continue
            print_canvas.create_rectangle(
                (50+(step[1]*50)), (50+(step[0]*50)), (50+((step[1]+1)*50)), (50+((step[0]+1)*50)), fill="#00ff00")
        print_canvas.pack()
        print_canvas.update()


if __name__ == '__main__':

    start_obj = PlannerNode()

    print("Number of steps taken by the bot are = ", len(start_obj.steps_taken))
    print("The length of path found by the bot is = ", len(start_obj.path))
    print("Path- ", start_obj.path)

    start_obj.current_obj.print_root.mainloop()