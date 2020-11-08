import numpy as np
import random


class NeuralNet:
    def __init__(self, NN_shape, width, height, unit, init_NN=True):
        self.width = width
        self.height = height
        self.unit = unit
        self.apple_position = ()
        self.theta = []
        self.bias = []
        if init_NN:
            self.initialize_weights(NN_shape)

    def collision_with_self(self, x, y, snake_position):
        if any(body == (x, y) for body in snake_position):
            return True
        return False


    def move(self, x, y, direction, prediction):
        unit = self.unit
        if direction == 'UP':
            if prediction == 1:
                return (x, y - unit), 'UP'
            elif prediction == 2:
                return (x - unit, y), 'LEFT'
            else:
                return (x + unit, y), 'RIGHT'
        elif direction == 'RIGHT':
            if prediction == 1:
                return (x + unit, y), 'RIGHT'
            elif prediction == 2:
                return (x, y - unit), 'UP'
            else:
                return (x, y + unit), 'DOWN'
        elif direction == 'DOWN':
            if prediction == 1:
                return (x, y + unit), 'DOWN'
            elif prediction == 2:
                return (x + unit, y), 'RIGHT'
            else:
                return (x - unit, y), 'LEFT'
        else:
            if prediction == 1:
                return (x - unit, y), 'LEFT'
            elif prediction == 2:
                return (x, y + unit), 'DOWN'
            else:
                return (x, y - unit), 'UP'

    def appleSense(self, x, y, dX, dY, foodX, foodY):
        if dX == 0:
            if foodX - x == 0 and (foodY - y)/dY > 0:
                return 1
        elif dY == 0:
            if foodY - y == 0 and (foodX - x)/dX > 0:
                return 1
        else:
            if (foodX - x)/dX == (foodY - y)/dY and (foodY - y)/dY > 0:
                return 1
        return 0

    def bodyCalculation(self, x, y, dX, dY, x2, y2):
        if dX == 0:
            if x2 - x == 0 and (y2 - y)/dY > 0:
                return (y2 - y)/dY
        elif dY == 0:
            if y2 - y == 0 and (x2 - x)/dX > 0:
                return (x2 - x)/dX
        else:
            if (x2 - x)/dX == (y2 - y)/dY and (y2 - y)/dY > 0:
                return (x2 - x)/dX
        return 10000

    def bodySense(self, x, y, dX, dY, snake_position):
        minDist = 10000
        for (body) in snake_position[1:]:
            minDist = min(minDist, self.bodyCalculation(x, y, dX, dY, body[0], body[1]))
        if minDist == 10000:
            return 0
        return 1/minDist

    def sense_in_direction2(self, x, y, dX, dY, foodX, foodY, snake_position):
        input = [0, 0]
        input[0] = self.appleSense(x, y, dX, dY, foodX, foodY)
        input[1] = self.bodySense(x, y, dX, dY, snake_position)
        return input

    def make_input2(self, x, y, foodX, foodY, snake_position):
        input = []

        input.extend(self.sense_in_direction2(x, y, 0, -self.unit, foodX,foodY, snake_position))  # check if self.unit is proper
        input.extend([1/y])

        input.extend(self.sense_in_direction2(x, y, self.unit, -self.unit, foodX, foodY, snake_position))
        input.extend([1/min(y, self.width-x)])

        input.extend(self.sense_in_direction2(x, y, self.unit, 0, foodX, foodY, snake_position))
        input.extend([1/(self.width-x)])

        input.extend(self.sense_in_direction2(x, y, self.unit,self.unit, foodX, foodY, snake_position))
        input.extend([1/min(self.height-y, self.width-x)])

        input.extend(self.sense_in_direction2(x, y, 0, self.unit, foodX, foodY, snake_position))
        input.extend([1/(self.height-y)])

        input.extend(self.sense_in_direction2(x, y, -self.unit,self.unit, foodX, foodY, snake_position))
        input.extend([1/min(x, self.height-y)])

        input.extend(self.sense_in_direction2(x, y, -self.unit, 0, foodX, foodY, snake_position))
        input.extend([1/x])

        input.extend(self.sense_in_direction2(x, y, -self.unit, -self.unit, foodX, foodY, snake_position))
        input.extend([1/min(y, x)])

        return input

    def sense_in_direction(self, x, y, dX, dY, foodX, foodY, snake_position):
        
        steps = 1
        food_along_direction = False
        collision_with_self = False
        input = [0, 0, 0]
        while ((x != 0) and (x != self.width - self.unit) and (y != 0) and (y != self.height-self.unit)):
            x, y = x+dX, y+dY
            steps += 1
            if(not food_along_direction and foodX == x and foodY == y):
                input[0] = 1
                food_along_direction = True
            if(not collision_with_self and self.collision_with_self(x, y, snake_position)):
                input[1] = 1 / steps
                collision_with_self = True
        input[2] = 1 / steps
        return input
    
    def make_input(self, x, y, foodX, foodY, snake, direction):
        input = []
        
        # look in direction where snake is moving
        (new_x, new_y), _ = self.move(x, y, direction, 1)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        # look in 90 degree left of direction where snake is moving
        (new_x, new_y), _ = self.move(x, y, direction, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        # look in 90 degree right of direction where snake is moving
        (new_x, new_y), _ = self.move(x, y, direction, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        # look in 45 degree left of direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 1)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        # look in 45 degree right of direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 1)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        # look in opposite to the direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 2)
        (new_x, new_y), new_dir = self.move(tempx, tempy, new_dir, 2)
        (new_x, new_y), _ = self.move(new_x, new_y, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        # look in 135 degree right of direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 3)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        # look in 135 degree left direction where snake is moving
        (tempx, tempy), new_dir = self.move(x, y, direction, 2)
        (new_x, new_y), _ = self.move(tempx, tempy, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.sense_in_direction(x, y, dir_x, dir_y, foodX, foodY, snake))
        return input

    def initialize_weights(self, NN_shape):
        for i in range(len(NN_shape)-1):
            theta = np.random.uniform(-0.5, 0.5,
                                      (NN_shape[i], NN_shape[i+1]))
            self.theta.append(theta)

            bias = np.random.uniform(-0.1, 0.1, (1, NN_shape[i+1]))
            self.bias.append(bias)

    def decision(self, x, y, snake_position, direction):
        foodX, foodY = self.apple_position
        input = self.make_input(x, y, foodX, foodY, snake_position, direction)
        input2 = self.make_input2(x, y, foodX, foodY, snake_position)
        
        input = np.array(input)
        outputs = []
        output = input
        for i in range(len(self.theta) - 1):
            output = self.relu(np.dot(output, self.theta[i]) + self.bias[i])
            outputs.append(output)
        output = self.softmax(
            np.dot(output, self.theta[i+1]) + self.bias[i+1])
        outputs.append(output)
        result = np.argmax(outputs[-1]) + 1
        return result

    # set the next apple_position variable

    def setNextFood(self, apple_position):
        self.apple_position = apple_position

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
