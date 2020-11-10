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
    
    def sigmoid(self, mat):
        return 1.0 / (1.0 + np.exp(-mat))

    def relu(self, mat):
        return mat * (mat > 0)

    def softmax(self, mat):
        mat = mat - np.max(mat)
        return np.exp(mat) / np.sum(np.exp(mat), axis=1)
    
    def collision_with_self(self, x, y, snake_position):
        if any(body == (x, y) for body in snake_position):
            return True
        return False

    def setNextFood(self, apple_position):
        self.apple_position = apple_position

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

    def sense_in_direction(self, x, y, dX, dY, foodX, foodY, snake_position):
        input = [0, 0]
        input[0] = self.appleSense(x, y, dX, dY, foodX, foodY)
        input[1] = self.bodySense(x, y, dX, dY, snake_position)
        return input

    def checkForZero(self, x):
        if x == 0:
            return 1
        return x
    
    def make_input(self, x, y, foodX, foodY, snake_position, direction):
        input = []

        input.extend(self.sense_in_direction(x, y, 0, -self.unit, foodX,foodY, snake_position)) 
        input.extend([self.unit/self.checkForZero((y-self.unit))])
        

        input.extend(self.sense_in_direction(x, y, self.unit, -self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero(min(y - self.unit, self.width - self.unit - x))])

        input.extend(self.sense_in_direction(x, y, self.unit, 0, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero((self.width - self.unit - x))])

        input.extend(self.sense_in_direction(x, y, self.unit,self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero(min(self.height - self.unit -y, self.width - self.unit - x))])

        input.extend(self.sense_in_direction(x, y, 0, self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero((self.height - self.unit -y))])

        input.extend(self.sense_in_direction(x, y, -self.unit,self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero(min(x - self.unit, self.height - self.unit -y))])

        input.extend(self.sense_in_direction(x, y, -self.unit, 0, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero((x - self.unit))])

        input.extend(self.sense_in_direction(x, y, -self.unit, -self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero(min((y-self.unit), (x - self.unit)))])
        
        if(direction == 'RIGHT'):
            input = input[6:] + input[:6]
        elif (direction == 'DOWN'):
            input = input[12:] + input[:12]
        elif (direction == 'LEFT'):
            input = input[18:] + input[:18]
        
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

