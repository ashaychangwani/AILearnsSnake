import numpy as np
import random


class NeuralNet:
    def __init__(self, layers, width, height, block_size, random_params=True):
        self.next_food = None
        self.outputs = []
        self.weights = []
        self.prev_res = -1
        self.bias = []
        self.prev_food_cost = 1.0
        self.block_size = block_size
        self.width = width
        self.height = height

        if random_params:
            for i in range(len(layers)-1):
                theta = np.random.uniform(-0.5, 0.5, (layers[i], layers[i+1]))
                self.weights.append(theta)

                bias = np.random.uniform(-0.1, 0.1, (1, layers[i+1]))
                self.bias.append(bias)

    def collision_with_self(self, x, y, snake_position):        
        for i in range(3, len(snake_position)-1):
            if snake_position[i][0] == x and snake_position[i][1] == y:
                return True
        return False

    def move(self, x, y, direction, result):            #remove because might be a copy of a snake.py fn
        l = self.block_size

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

    def look(self, x, y, direction_x, direction_y, fx, fy, snake_position):
        distance = 1
        input = [0, 0, 0]
        found_food = False
        body_found = False
        while ((x != 0) and (x != self.width - self.block_size) and (y != 0) and (y != self.height-self.block_size)):
            x, y = x+direction_x, y+direction_y
            distance += 1
            if(not found_food and fx == x and fy == y):
                input[0] = 1
                found_food = True
            if(not body_found and self.collision_with_self(x, y, snake_position)):
                input[1] = 1 / distance
                body_found = True
        input[2] = 1 / distance
        return input

    def make_input(self, x, y, fx, fy, snake, direction):
        input = []
        # look in direction where snake is moving
        (new_x, new_y), _ = self.move(x, y, direction, 1)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 90 degree left of direction where snake is moving
        (new_x, new_y), _ = self.move(x, y, direction, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 90 degree right of direction where snake is moving
        (new_x, new_y), _ = self.move(x, y, direction, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 45 degree left of direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 1)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 45 degree right of direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 1)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        # look in opposite to the direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 2)
        (new_x, new_y), new_dir = self.move(tempx, tempy, new_dir, 2)
        (new_x, new_y), _ = self.move(new_x, new_y, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 135 degree right of direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 3)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 135 degree left direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 2)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look(x, y, dir_x, dir_y, fx, fy, snake))
        return input

    def decision(self, x, y, snake_position, direction):
        fx, fy = self.next_food
        input = self.make_input(x, y, fx, fy, snake_position, direction)
        input = np.array(input)

        output = input
        for i in range(len(self.weights) - 1):
            output = self.relu(np.dot(output, self.weights[i]) + self.bias[i])
            self.outputs.append(output)
        output = self.softmax(np.dot(output, self.weights[i+1]) + self.bias[i+1])
        self.outputs.append(output)
        result = np.argmax(self.outputs[-1]) + 1
        return result

    

    # set the next food variable
    def setNextFood(self, food):
        self.next_food = food

    # sigmoid activation functions
    def sigmoid(self, mat):
        return 1.0 / (1.0 + np.exp(-mat))

    # relu activation function
    def relu(self, mat):
        return mat * (mat > 0)

    # softmax function
    def softmax(self, mat):
        mat = mat - np.max(mat)
        return np.exp(mat) / np.sum(np.exp(mat), axis=1)