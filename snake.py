from pygame import draw
from neuralnet import NeuralNet
import random


class snake:
    def __init__(self, width, height, layers, block_size, random_params=True, random_start=True):
        self.snake_position = []
        self.width = width
        self.height = height
        self.steps_taken = 0
        self.no_of_same_result = 0
        self.collision_with_boundary = False
        self.collision_with_self = False
        self.block_size = block_size

        self.neuralnet = NeuralNet(
            layers, self.width, self.height, self.block_size, random_params)

        if random_start:
            self.direction = random.choice(['east', 'north', 'south', 'west'])
            x = random.randint(3*block_size, width - 3*block_size)
            self.head_x = x - (x % block_size)
            y = random.randint(3*block_size, height - 3*block_size)
            self.head_y = y - (y % block_size)
        else:
            self.direction = 'east'
            self.head_x, self.head_y = 40, 40
        self.snake_position.append((self.head_x, self.head_y))

    def draw_snake(self, playground, color):
        l = self.block_size
        for (x, y) in self.snake_position:
            draw.rect(playground, color, (x, y, l, l), 1)
            draw.rect(playground, color, (x+3, y+3, l-6, l-6))
        return playground

    def isAlive(self):
        if not self.collision_with_self and not self.collision_with_boundary:
            return True
        return False

    def check_north(self):
        if self.head_y - self.block_size < self.block_size:
            self.collision_with_boundary = True
        for i in range(len(self.snake_position) - 1):
            if self.snake_position[i][0] == self.head_x and self.snake_position[i][1] == (self.head_y - self.block_size):
                self.collision_with_self = True

    # move the snake in north
    def move_north(self):
        self.check_north()
        if not (self.collision_with_boundary or self.collision_with_self):
            self.direction = 'north'
            self.head_y = self.head_y - self.block_size
            self.snake_position.insert(0, (self.head_x, self.head_y))
            self.snake_position.pop()

    # sets the collision_with_boundary and collision_with_self if unable to go south accordingly
    def check_south(self):
        if self.head_y + self.block_size >= self.height - self.block_size:
            self.collision_with_boundary = True
        for i in range(len(self.snake_position) - 1):
            if self.snake_position[i][0] == self.head_x and self.snake_position[i][1] == (self.head_y + self.block_size):
                self.collision_with_self = True

    # move the snake in south
    def move_south(self):
        self.check_south()
        if not (self.collision_with_boundary or self.collision_with_self):
            self.direction = 'south'
            self.head_y = self.head_y + self.block_size
            self.snake_position.insert(0, (self.head_x, self.head_y))
            self.snake_position.pop()

    # sets the collision_with_boundary and collision_with_self if unable to go east accordingly
    def check_east(self):
        if self.head_x + self.block_size >= self.width - self.block_size:
            self.collision_with_boundary = True
        for i in range(len(self.snake_position) - 1):
            if self.snake_position[i][0] == (self.head_x + self.block_size) and self.snake_position[i][1] == self.head_y:
                self.collision_with_self = True

    # move the snake in east
    def move_east(self):
        self.check_east()
        if not (self.collision_with_boundary or self.collision_with_self):
            self.direction = 'east'
            self.head_x = self.head_x + self.block_size
            self.snake_position.insert(0, (self.head_x, self.head_y))
            self.snake_position.pop()

    # sets the collision_with_boundary and collision_with_self if unable to go west accordingly
    def check_west(self):
        if self.head_x - self.block_size < self.block_size:
            self.collision_with_boundary = True
        for i in range(len(self.snake_position) - 1):
            if self.snake_position[i][0] == (self.head_x - self.block_size) and self.snake_position[i][1] == self.head_y:
                self.collision_with_self = True

    # move the snake in west
    def move_west(self):
        self.check_west()
        if not (self.collision_with_boundary or self.collision_with_self):
            self.direction = 'west'
            self.head_x = self.head_x - self.block_size
            self.snake_position.insert(0, (self.head_x, self.head_y))
            self.snake_position.pop()

    def getNextPos(self, result):
        l = self.block_size
        x = self.head_x
        y = self.head_y
        direction = self.direction
        if direction == 'north':
            if result == 1:
                return (x, y - l), 'north'
            elif result == 2:
                return (x - l, y), 'west'
            else:
                return (x + l, y), 'east'
        elif direction == 'east':
            if result == 1:
                return (x + l, y), 'east'
            elif result == 2:
                return (x, y - l), 'north'
            else:
                return (x, y + l), 'south'
        elif direction == 'south':
            if result == 1:
                return (x, y + l), 'south'
            elif result == 2:
                return (x + l, y), 'east'
            else:
                return (x - l, y), 'west'
        else:
            if result == 1:
                return (x - l, y), 'west'
            elif result == 2:
                return (x, y + l), 'south'
            else:
                return (x, y - l), 'north'

    def check_collision_with_self(self, x, y):
        for i in range(3, len(self.snake_position)-1):
            if self.snake_position[i][0] == x and self.snake_position[i][1] == y:
                return True
        return False
    
    def updateSnakePosition(self,result):
        pos, dir = self.getNextPos(result)
        if(pos[0] != 0) and (pos[0] != self.width - self.block_size) and (pos[1] != 0) and (pos[1] != self.height - self.block_size) and (not self.check_collision_with_self(pos[0], pos[1])):
            self.head_x, self.head_y = pos[0], pos[1]
            self.snake_position.insert(0, (self.head_x, self.head_y))
            self.direction = dir 
            return True
        return False
    
    def move(self, result):
        if self.direction == 'north':
            if result == 1:
                self.move_north()
            elif result == 2:
                self.move_west()
            else:
                self.move_east()
        elif self.direction == 'east':
            if result == 1:
                self.move_east()
            elif result == 2:
                self.move_north()
            else:
                self.move_south()
        elif self.direction == 'south':
            if result == 1:
                self.move_south()
            elif result == 2:
                self.move_east()
            else:
                self.move_west()
        else:
            if result == 1:
                self.move_west()
            elif result == 2:
                self.move_south()
            else:
                self.move_north()
        self.steps_taken += 1
        return self.isAlive()
    
            
    
