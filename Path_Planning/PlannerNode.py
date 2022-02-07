import sys
import random
from MapNode import MapNode
from MapClass import Map
import numpy as np
import tkinter
import time


def get_dir_backward(dir_forward):
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
        # Since we know that the first step the bot will take will be down, we can simply do it here
        self.current_obj.direction_callback("down")  # example 1
        self.current_direction = 'down'
        self.steps = 1
        self.visited = np.zeros(
            (self.current_obj.walls.height, self.current_obj.walls.width))
        self.blocked_places = []
        self.steps_taken = [self.current_obj.current]
        self.wall_callback()

    def wall_callback(self):
        # current_obj has all the attributes to help you in in your path planning !
        # Your code goes here. You need to figure out an algorithm to decide on the best direction of movement of the bot based on the data you have.
        # after deciding on the direction, you need to call the direction_callback() function as done in example 1.
        # dir=['up','down','left','right']
        while self.current_obj.current != self.current_obj.walls.end:
            walls = self.current_obj.walls
            position = self.current_obj.current
            self.visited[position[0]][position[1]] += 1
            dirs = ['left', 'right', 'up', 'down']
            if(walls.check_left_wall(position)):
                dirs.remove('left')
            if(walls.check_right_wall(position)):
                dirs.remove('right')
            if(walls.check_top_wall(position)):
                dirs.remove('up')
            if(walls.check_bottom_wall(position)):
                dirs.remove('down')
            dir_prob = {}
            for dir in dirs:
                dir_prob[dir] = 0
                next_pos = self.get_next_position(dir)
                dir_prob[dir] -= self.visited[next_pos[0]][next_pos[1]]
                if self.visited[next_pos[0]][next_pos[1]] == 0:
                    dir_prob[dir] += 1
                if next_pos == self.current_obj.walls.end:
                    dir_prob[dir] += 1000
                if self.get_next_position(dir) in self.blocked_places:
                    dir_prob[dir] -= 1000
            v = list(dir_prob.values())
            max_prob_dir = []
            for dir in dir_prob:
                if dir_prob[dir] == max(v):
                    max_prob_dir.append(dir)
            dir = random.choice(max_prob_dir)
            # dir=max_prob_dir[0]
            self.current_obj.direction_callback(dir)
            if self.current_obj.current in self.steps_taken:
                self.blocked_places.append(position)

            self.steps_taken.append(self.current_obj.current)
            self.steps += 1
        self.make_path()

    def get_next_position(self, direction):
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

    def make_path(self):
        steps = self.steps_taken
        # for i,step in enumerate(steps):
        #    for j,step1 in enumerate(steps[i:]):
        #        if step==step1:
        #            del steps[i:j]
        width = self.current_obj.walls.width
        height = self.current_obj.walls.height
        print(self.steps_taken)
        print(self.steps)
        print_root = tkinter.Tk()
        print_canvas = tkinter.Canvas(
            print_root, bg="white", height=50+height*50, width=50+width*50)
        for step in self.steps_taken:
            print_canvas.create_rectangle(
                (50+(step[1]*50)), (50+(step[0]*50)), (50+((step[1]+1)*50)), (50+((step[0]+1)*50)), fill="#00ff00")
        print_canvas.pack()
        print_canvas.update()
        print_root.mainloop()


if __name__ == '__main__':
    start_obj = PlannerNode()
    start_obj.current_obj.print_root.mainloop()
