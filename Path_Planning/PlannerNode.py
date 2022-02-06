import sys
import random
from MapNode import MapNode
from MapClass import Map

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
        self.visited_places=[]
        self.wall_callback()
        

    def wall_callback(self):
        # current_obj has all the attributes to help you in in your path planning !
        # Your code goes here. You need to figure out an algorithm to decide on the best direction of movement of the bot based on the data you have.
        # after deciding on the direction, you need to call the direction_callback() function as done in example 1.
        # dir=['up','down','left','right']
            walls=self.current_obj.walls
            position=self.current_obj.current
            self.visited_places.append(position)
            dirs=['left','right','up','down']
            if(walls.check_left_wall(position) or self.get_next_position('left') in self.visited_places):
                dirs.remove('left')
            if(walls.check_right_wall(position) or self.get_next_position('right') in self.visited_places):
                dirs.remove('right')
            if(walls.check_top_wall(position) or self.get_next_position('up') in self.visited_places):
                dirs.remove('up')
            if(walls.check_bottom_wall(position) or self.get_next_position('down') in self.visited_places):
                dirs.remove('down')
            if dirs:    
                self.current_obj.direction_callback(random.choice(dirs))
            else:
                dirs=['left','right','up','down']
                if(walls.check_left_wall(position)):
                    dirs.remove('left')
                if(walls.check_right_wall(position)):
                    dirs.remove('right')
                if(walls.check_top_wall(position)):
                    dirs.remove('up')
                if(walls.check_bottom_wall(position)):
                    dirs.remove('down')
                self.current_obj.direction_callback(random.choice(dirs))
                
            self.steps+=1
            print(self.steps)
            self.wall_callback()
    
    
    def get_next_position(self,direction):
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


if __name__ == '__main__':
    start_obj = PlannerNode()
    start_obj.current_obj.print_root.mainloop()
