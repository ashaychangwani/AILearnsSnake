import numpy as np
import random


class NeuralNet:
    def __init__(self, NN_shape, display_width, display_height, unit, init_NN=True):
        """Initializes a class of type NeuralNet.

        Args:
            NN_shape (list): Shape of the neural network architecure
            display_width (int): Width of display in pixels
            display_height (int): Height of display in pixels
            unit (int): Size of each unit 
            init_NN (bool, optional): Whether the neural network should be initalized with random weights. Defaults to True.
        """
        self.display_width = display_width
        self.display_height = display_height
        self.unit = unit
        self.apple_position = ()
        self.theta = []
        self.bias = []
        if init_NN:
            self.initialize_weights(NN_shape)
    
    def sigmoid(self, mat):
        """Performs sigmoid operation

        Args:
            mat (matrix): Input matrix

        Returns:
            [matrix]: result which is sigmoid(matrix)
        """
        return 1.0 / (1.0 + np.exp(-mat))

    def relu(self, mat):
        """Performs ReLU operation

        Args:
            mat (matrix): Input matrix

        Returns:
            [matrix]: result which is ReLU(matrix)
        """
        return mat * (mat > 0)

    def softmax(self, mat):
        """Performs Softmax operation

        Args:
            mat (matrix): Input matrix

        Returns:
            [matrix]: result which is softmax(matrix)
        """
        mat = mat - np.max(mat)
        return np.exp(mat) / np.sum(np.exp(mat), axis=1)

    def setNextFood(self, apple_position):
        """Sets the next location for the apple

        Args:
            apple_position ([list]): List of x and y coordinates of apple
        """
        self.apple_position = apple_position

    def appleSense(self, x, y, dX, dY, foodX, foodY):
        """Check if apple is present along current direction

        Args:
            x ([int]): X coordinate of snake_head
            y ([int]): Y coordinate of snake_head
            dX ([int]): Direction of movement of snake in x-direction
            dY ([int]): Direction of movement of snake in y-direction
            foodX ([int]): X coordinate of food
            foodY ([int]): Y coordinate of food

        Returns:
            [boolean]: Represents 1 if food is present along path, else 0
        """
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
        """Checks if specified part of snake's body is present along chosen direction

        Args:
            x ([int]): X coordinate of selected body part of snake
            y ([int]): Y coordinate of snake_head
            dX ([int]): Direction of movement of snake in x-direction
            dY ([int]): Direction of movement of snake in y-direction
            x2 ([int]): [description]
            y2 ([int]): Y coordinate of selected body part of snake

        Returns:
            [type]: [description]
        """
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
        """Check if any part of the body of the snake exists along chosen 
           direction

        Args:
            x ([int]): X coordinate of selected body part of snake
            y ([int]): Y coordinate of snake_head
            dX ([int]): Direction of movement of snake in x-direction
            dY ([int]): Direction of movement of snake in y-direction
            snake_position ([list]): List of the body parts of the snake

        Returns:
            [int]: Normalized distance between snake_head and closest part of the snake's body
                   along chosen direction
        """
        minDist = 10000
        for (body) in snake_position[1:]:
            minDist = min(minDist, self.bodyCalculation(x, y, dX, dY, body[0], body[1]))
        if minDist == 10000:
            return 0
        return 1/minDist

    def sense_in_direction(self, x, y, dX, dY, foodX, foodY, snake_position):
        """Sense for apple and body parts in selected direction

        Args:
            x ([int]): X coordinate of selected body part of snake
            y ([int]): Y coordinate of snake_head
            dX ([int]): Direction of movement of snake in x-direction
            dY ([int]): Direction of movement of snake in y-direction
            foodX ([int]): X coordinate of apple
            foodY ([int]): Y coordinate of apple
            snake_position ([list]): list of the positions of the snake's body

        Returns:
            [list]: 2 values containing results for apple and body part respectively
        """
        input = [0, 0]
        input[0] = self.appleSense(x, y, dX, dY, foodX, foodY)
        input[1] = self.bodySense(x, y, dX, dY, snake_position)
        return input

    def checkForZero(self, x):
        """Checks for 0 to avoid division by 0 errors

        Args:
            x ([int]): Input

        Returns:
            [int]: Output
        """
        if x == 0:
            return 1
        return x
    
    def make_input(self, x, y, foodX, foodY, snake_position, direction):
        """Function to sense in all directions and produce the input for the neural network

        Args:
            x ([int]): x coordinate of snake head
            y ([int]): y coordinate of snake head
            foodX ([int]): x coordinate of food
            foodY ([int]): y coordinate of food
            snake_position ([list]): List of coordinates of snake's body
            direction ([int]): previous direction

        Returns:
            [list]: List of length 24 representing the 3 inputs in each of 8 directions 
        """
        input = []

        input.extend(self.sense_in_direction(x, y, 0, -self.unit, foodX,foodY, snake_position)) 
        input.extend([self.unit/self.checkForZero((y-self.unit))])
        

        input.extend(self.sense_in_direction(x, y, self.unit, -self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero(min(y - self.unit, self.display_width - self.unit - x))])

        input.extend(self.sense_in_direction(x, y, self.unit, 0, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero((self.display_width - self.unit - x))])

        input.extend(self.sense_in_direction(x, y, self.unit,self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero(min(self.display_height - self.unit -y, self.display_width - self.unit - x))])

        input.extend(self.sense_in_direction(x, y, 0, self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero((self.display_height - self.unit -y))])

        input.extend(self.sense_in_direction(x, y, -self.unit,self.unit, foodX, foodY, snake_position))
        input.extend([self.unit/self.checkForZero(min(x - self.unit, self.display_height - self.unit -y))])

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
        """Initialize weights of the neural network

        Args:
            NN_shape ([list]): Shape of the neural network
        """
        for i in range(len(NN_shape)-1):
            theta = np.random.uniform(-0.5, 0.5,
                                      (NN_shape[i], NN_shape[i+1]))
            self.theta.append(theta)

            bias = np.random.uniform(-0.1, 0.1, (1, NN_shape[i+1]))
            self.bias.append(bias)

    def decision(self, x, y, snake_position, direction):
        """Run inputs through neural network to get the output as the decision of 
        

        Args:
            x (int): X coordinate of snake_head
            y (int): Y Coordinate of snake_head
            snake_position (list): List of the coordinates of snake's body
            direction (str): String representing the previous direction 

        Returns:
            int: Integer output of the neural network
        """
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

