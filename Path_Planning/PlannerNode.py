
import sys
import random
import numpy as np
from MapNode import MapNode
import tkinter
import math

def get_dir_backward(dir_forward):
    '''Returns the direction opposite to input direction'''

    if(dir_forward == 'right'):
        return 'left'

    if(dir_forward == 'down'):
        return 'up'

    if(dir_forward == 'left'):
        return 'right'

    if(dir_forward == 'up'):
        return 'down'


class PlannerNode:
    def __init__(self):
        self.current_obj = MapNode()
        self.visited_points = list(self.current_obj.current)
        self.current_dir="down"
        self.visited = np.zeros(
            (self.current_obj.walls.height, self.current_obj.walls.width))
        self.blocked_places = []
        self.wall_callback()

    def wall_callback(self):

        while self.current_obj.current != self.current_obj.walls.end:
            position = self.current_obj.current
            self.visited[position[0]][position[1]] += 1
            next_step = self.get_next_step()
            self.current_dir=self.get_dir(next_step)
            self.take_step(next_step)
            self.visited_points.append(self.current_obj.current)
        self.path=self.make_path(self.current_obj.walls.start)
        self.show_path(self.path)

    def get_next_step(self):

        x0, y0 = self.current_obj.current
        points = [(x0, y0-1), (x0, y0+1), (x0-1, y0), (x0+1, y0)]

        cost_map = {}

        for point in points:
            if self.current_obj.walls.check_coords(point) and self.is_step_valid(point):
                cost_map[point] = self.get_cost(point)

        v = list(cost_map.values())

        min_cost_points = []

        for point in cost_map:
            if cost_map[point] == min(v):
                min_cost_points.append(point)
        
        for point in min_cost_points:
            if(self.get_dir(point)==self.current_dir):
                return point

        point=self.secondary_decision_maker(min_cost_points)
        return point

    def get_cost(self, point):
        end = self.current_obj.walls.end

        a = np.zeros((self.current_obj.walls.height,
                     self.current_obj.walls.width), dtype=np.uint32)

        a[point[0]][point[1]] = 1

        k = 0

        while a[end[0]][end[1]] == 0:
            k += 1

            for i in range(len(a)):
                for j in range(len(a[i])):

                    if a[i][j] == k:

                        if i > 0 and a[i-1][j] == 0:
                            if (i, j) in self.visited_points and self.current_obj.walls.check_top_wall((i, j)):
                                pass
                            else:
                                a[i-1][j] = k+1

                        if j > 0 and a[i][j-1] == 0:
                            if (i, j) in self.visited_points and self.current_obj.walls.check_left_wall((i, j)):
                                pass
                            else:
                                a[i][j-1] = k+1

                        if i < len(a)-1 and a[i+1][j] == 0:
                            if (i, j) in self.visited_points and self.current_obj.walls.check_bottom_wall((i, j)):
                                pass
                            else:
                                a[i+1][j] = k+1

                        if j < len(a[i])-1 and a[i][j+1] == 0:
                            if (i, j) in self.visited_points and self.current_obj.walls.check_right_wall((i, j)):
                                pass
                            else:
                                a[i][j+1] = k+1
        k = a[end[0]][end[1]]
        return k

    def is_step_valid(self, final_pos):
        x0, y0 = self.current_obj.current
        x1, y1 = final_pos
        if y1-y0 < 0:
            return not (self.current_obj.walls.check_left_wall((x0, y0)))
        if y1-y0 > 0:
            return not (self.current_obj.walls.check_right_wall((x0, y0)))
        if x1-x0 > 0:
            return not (self.current_obj.walls.check_bottom_wall((x0, y0)))
        if x1-x0 < 0:
            return not (self.current_obj.walls.check_top_wall((x0, y0)))
    
    def get_next_position(self, direction):
        '''returns the position bot will be at if it moves in the geiven direction'''

        if direction == 'up':
            if self.current_obj.current[0] >= 1:
                return (self.current_obj.current[0]-1, self.current_obj.current[1])

        elif direction == 'left':
            if self.current_obj.current[1] >= 1:
                return (self.current_obj.current[0], self.current_obj.current[1]-1)

        elif direction == 'right':
            return (self.current_obj.current[0], self.current_obj.current[1]+1)

        elif direction == 'down':
            return (self.current_obj.current[0]+1, self.current_obj.current[1])

    def take_step(self, final_pos):
        x0, y0 = self.current_obj.current
        x1, y1 = final_pos
        if y1-y0 < 0:
            # print("left")
            self.current_obj.direction_callback("left")
        if y1-y0 > 0:
            # print("right")
            self.current_obj.direction_callback("right")
        if x1-x0 > 0:
            # print("down")
            self.current_obj.direction_callback("down")
        if x1-x0 < 0:
            # print("up")
            self.current_obj.direction_callback("up")
    
    def get_dir(self, final_pos):
        x0, y0 = self.current_obj.current
        x1, y1 = final_pos
        if y1-y0 < 0:
            return "left"
        if y1-y0 > 0:
            return "right"
        if x1-x0 > 0:
            return "down"
        if x1-x0 < 0:
            return "up"
    
    def secondary_decision_maker(self,min_cost_points):
        dirs=[]
        for point in min_cost_points:
            dirs.append(self.get_dir(point))
        # to decide the best direction to be taken
        dir_prob = {}

        for dir in dirs:

            dir_prob[dir] = 0

            # where the bot would be if the step is taken
            next_pos = self.get_next_position(dir)

            # penalize if the next point is already visited
            dir_prob[dir] -= self.visited[next_pos[0]][next_pos[1]]

            # visit unvisited places to explore the map.
            if self.visited[next_pos[0]][next_pos[1]] == 0:
                dir_prob[dir] += 10

            # if next step is end take it.
            if next_pos == self.current_obj.walls.end:
                dir_prob[dir] += 1000

            # avoid blocked places at all cost
            if self.get_next_position(dir) in self.blocked_places:
                dir_prob[dir] -= 100000

            # try to get closer to the end in every step
            if self.closer_to_end(dir):
                dir_prob[dir] += 2

            # a path of length 2 is most probably a loop,so avoid taking it.
            if len(dir) == 2:
                dir_prob[dir] -= 10
            

        v = list(dir_prob.values())

        # stores the directions with maximum probability.
        max_prob_dir = []

        for dir in dir_prob:
            if dir_prob[dir] == max(v):
                max_prob_dir.append(dir)

        # From the directions who have maximum probability,choose a random one
        dir = random.choice(max_prob_dir)
        point= min_cost_points[dirs.index(dir)]
        print(point)
        return(point)
    
    def closer_to_end(self, dir):
        '''returns true if the bot move closer to the end if it moves in the given direction'''

        end = self.current_obj.walls.end

        current = self.current_obj.current
        next = self.get_next_position(dir)

        dist0 = math.sqrt((current[0]-end[0])**2+(current[1]-end[1])**2)
        dist1 = math.sqrt((next[0]-end[0])**2+(next[1]-end[1])**2)

        return dist1 < dist0
    
    def make_path(self,start):
        '''Makes the most optimal path given the steps_taken by the bot in reaching the end'''
        # Alogrithm-
        # 1.Only consider the points where the bot has been to,others are pseudo walls.
        # 2.Put a 1 at starting point.
        # 3.Everywhere around 1,put 2 if no wall
        # 4.Everywhere around 2, put 3 if no wall
        # 5.Continue till we reach the end
        # 6.The number at the end is the actual path length

        steps = self.visited_points
        end = self.current_obj.walls.end

        a = np.ones((self.current_obj.walls.height,
                    self.current_obj.walls.width),
                    dtype=np.uint32)

        for x in range(self.current_obj.walls.height):
            for y in range(self.current_obj.walls.width):

                if (x, y) in steps:
                    a[x][y] = 0

        # start with a blank matrix
        m = np.zeros_like(a)

        # assign one to the starting point
        m[start[0]][start[1]] = 1

        # the counter of steps
        k = 0

        while m[end[0]][end[1]] == 0:

            # take the next step
            k += 1

            # the following nested loops are used to make one step
            for i in range(len(m)):
                for j in range(len(m[i])):

                    # use this object to get the walls' info at the given point.
                    walls = self.current_obj.walls

                    # if we find the value of some point equal to k->
                    if m[i][j] == k:

                        # if there is no number yet,and there is no wall(including pseudo wall),
                        # set k+1 to that cell

                        if i > 0 and m[i-1][j] == 0 and a[i-1][j] == 0 and not walls.check_top_wall((i, j)):
                            m[i-1][j] = k + 1

                        if j > 0 and m[i][j-1] == 0 and a[i][j-1] == 0 and not walls.check_left_wall((i, j)):
                            m[i][j-1] = k + 1

                        if i < len(m)-1 and m[i+1][j] == 0 and a[i+1][j] == 0 and not walls.check_bottom_wall((i, j)):
                            m[i+1][j] = k + 1

                        if j < len(m[i])-1 and m[i][j+1] == 0 and a[i][j+1] == 0 and not walls.check_right_wall((i, j)):
                            m[i][j+1] = k + 1
        # now we need to find the shortest path based on the m-matrix

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
        print_root.mainloop()


if __name__ == '__main__':
    start_obj = PlannerNode()
    
    print("Number of steps taken by the bot are = ", len(start_obj.visited_points))
    print("The length of path found by the bot is = ", len(start_obj.path))
    print("Path- ", start_obj.path)
    
    start_obj.current_obj.print_root.mainloop()