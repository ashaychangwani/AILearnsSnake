from pygame import draw, image, transform
from nn import NeuralNet
import random


class Environment:
    def __init__(self, display_height, display_width, unit_size):
        """Creates an object of type Environment.

        Args:
            display_height (int): Height of display in pixels.
            display_width (int): Width of display in pixels.
            unit_size (int): Size of each block in pixels.
        """
        self.display_height = display_height
        self.display_width = display_width
        self.unit = unit_size
        self.apple_position = (0, 0)

    def draw_apple(self, environment, color):
        """Draw apple on the screen

        Args:
            environment (object): Instance of type Environment
            color (tuple): RGB values of colour

        Returns:
            environment: Returns instance of type Environment after drawing apple
        """
        apple_image = image.load('apple.png')
        apple_image = transform.scale(apple_image, (10, 10))
        environment.blit(
            apple_image, (self.apple_position[0], self.apple_position[1], self.unit, self.unit))
        return environment

    def draw_boundary(self, environment, color):
        """Draws boundary on the screen

        Args:
            environment (object): Instance of type Environment
            color (tuple): RGB values of colour
        """
        unit = self.unit
        for w in range(0, self.display_width, self.unit):
            draw.rect(environment, color, (w, 0, unit, unit))
            draw.rect(environment, color,
                             (w, self.display_height - unit, unit, unit))
        for h in range(0, self.display_height, self.unit):
            draw.rect(environment, color, (0, h, unit, unit))
            draw.rect(environment, color,
                             (self.display_width - unit, h, unit, unit))

    def create(self, environment, color):
        """Initialize the environment and draw boundaries

        Args:
            environment (object): Instance of type Environment
            color (tuple): RGB values of colour

        Returns:
            environment: Returns instance of type Environment after drawing apple
        """
        environment.fill((200, 200, 200))
        self.draw_boundary(environment, color)
        return environment

    def create_new_apple(self, snake_position):
        """Creates new apple, checks that the new apple does not appear on the body of the snake

        Args:
            snake_position (list): List of the snake body coordinates

        Returns:
            list: Coordinates of new apple position
        """
        unit = self.unit
        apple_position = (unit*random.randint(2, self.display_width/unit - 2),
                          unit*random.randint(2, self.display_height/unit - 2))
        while any(body == apple_position for body in snake_position):
            apple_position = (unit*random.randint(2, self.display_width/unit - 2),
                              unit*random.randint(2, self.display_height/unit - 2))
        self.apple_position = apple_position
        return self.apple_position

class snake:
    def __init__(self, display_width, display_height, NN_shape, unit, init_NN=True, random_start=True):
        """Initializes an object of type snake

        Args:
            display_height (int): Height of display in pixels.
            display_width (int): Width of display in pixels.
            NN_shape (list): Shape of neural network architecure
            unit_size (int): Size of each block in pixels.
            init_NN (bool, optional): Initalize neural network with random weights. Defaults to True.
            random_start (bool, optional): Start the snake position randomly or at predefined location. Defaults to True.
        """
        self.snake_position = []
        self.display_width = display_width
        self.display_height = display_height
        self.time_since_apple = 0
        self.collision_with_boundary = False
        self.collision_with_self = False
        self.unit = unit

        self.neuralnet = NeuralNet(
            NN_shape, self.display_width, self.display_height, self.unit, init_NN)

        self.snake_position.append(self.initSnake(random_start))

    def initSnake(self, random_start):
        """Set the start position and direction of snake

        Args:
            random_start (bool): Describes whether the snake should start randomly or

        Returns:
            tuple: X and Y coordinates of snake_head (starting position)
        """
        if random_start:
            self.direction = random.choice(['RIGHT', 'UP', 'DOWN', 'LEFT'])
            self.head_x = random.randint(
                3,  self.display_width / self.unit - 3) * self.unit
            self.head_y = random.randint(
                3,  self.display_height / self.unit - 3) * self.unit
        else:
            self.direction = 'RIGHT'
            self.head_x, self.head_y = 40, 40
        return (self.head_x, self.head_y)

    def isAlive(self):
        """Check if snake is alive
    
        Returns:
            bool: True if alive, False otherwise
        """
        if not self.collision_with_self and not self.collision_with_boundary:
            return True
        return False
    
    def eatApple(self, direction):
        """Add the location to snake body and increase snake size by 1

        Args:
            direction (str): Direction of movement after eating apple
        """
        self.snake_position.insert(0, (self.head_x, self.head_y))
        self.move(direction)
        
    def eatAppleHuman(self, direction):
        """Eat Apple method but for player playing the game instead of AI

        Args:
            direction (str): Direction of movement after eating apple
        """
        self.snake_position.insert(0, (self.head_x, self.head_y))
        self.moveHuman(direction)

    def moveInDirection(self, direction):
        """Move the snake in a particular direction, if chosen direction is valid. Else keep moving in current direction.

        Args:
            direction (str): Direction chosen by user
        """
        if direction == 'UP':
            self.head_y = self.head_y - self.unit
        elif direction == 'DOWN':
            self.head_y = self.head_y + self.unit
        elif direction == 'LEFT':
            self.head_x = self.head_x - self.unit
        else:
            self.head_x = self.head_x + self.unit
        self.direction = direction
        self.snake_position.insert(0, (self.head_x, self.head_y))
        self.snake_position.pop()
        self.check_valid()

    def check_valid(self):
        """Check if the snake is alive / has crashed into it's own body or boundary
        """
        if self.head_x == self.unit or self.head_x == self.display_width - self.unit or self.head_y == self.unit or self.head_y == self.display_height - self.unit:
            self.collision_with_boundary = True
        for (body_x, body_y) in self.snake_position[1:]:
            if body_x == self.head_x and body_y == self.head_y:
                self.collision_with_self = True

    def move(self, result):
        """Move the snake in a chosen direction

        Args:
            result (int): Direction chosen by the AI for movement of the snake

        Returns:
            bool: Describes whether or not snake is alive after movement
        """
        if self.direction == 'UP':
            if result == 1:
                self.moveInDirection('UP')
            elif result == 2:
                self.moveInDirection('LEFT')
            else:
                self.moveInDirection('RIGHT')
        elif self.direction == 'RIGHT':
            if result == 1:
                self.moveInDirection('RIGHT')
            elif result == 2:
                self.moveInDirection('UP')
            else:
                self.moveInDirection('DOWN')
        elif self.direction == 'DOWN':
            if result == 1:
                self.moveInDirection('DOWN')
            elif result == 2:
                self.moveInDirection('RIGHT')
            else:
                self.moveInDirection('LEFT')
        else:
            if result == 1:
                self.moveInDirection('LEFT')
            elif result == 2:
                self.moveInDirection('DOWN')
            else:
                self.moveInDirection('UP')
        self.time_since_apple += 1
        return self.isAlive()

    def moveHuman(self, result):
        """Move the snake in a chosen direction for player, not for AI

        Args:
            result (int): Direction chosen by the player for movement of the snake

        Returns:
            bool: Describes whether or not snake is alive after movement
        """
        if self.direction == 'UP':
            if result == 1:
                self.moveInDirection('UP')
            elif result == 2:
                self.moveInDirection('LEFT')
            elif result == 3:
                self.moveInDirection('RIGHT')
        elif self.direction == 'RIGHT':
            if result == 1:
                self.moveInDirection('UP')
            elif result == 3:
                self.moveInDirection('RIGHT')
            elif result == 4:
                self.moveInDirection('DOWN')
        elif self.direction == 'DOWN':
            if result == 2:
                self.moveInDirection('LEFT')
            elif result == 3:
                self.moveInDirection('RIGHT')
            elif result == 4:
                self.moveInDirection('DOWN')
        elif self.direction == 'LEFT':
            if result == 1:
                self.moveInDirection('UP')
            elif result == 2:
                self.moveInDirection('LEFT')
            elif result == 4:
                self.moveInDirection('DOWN')
        elif result!=0:
            self.moveInDirection(self.direction)
        return self.isAlive()
        
    def convAIToDirections(self, result):
        """Convert relative integer output by AI helper into absolute direction for the

        Args:
            result ([int]): Direction as output by the AI helper    

        Returns:
            str : Absolute direction 
        """
        if self.direction == 'UP':
            if result == 1:
                return 'UP'
            elif result == 2:
                return 'LEFT'
            else:
                return 'RIGHT'
        elif self.direction == 'RIGHT':
            if result == 1:
                return 'RIGHT'
            elif result == 2:
                return 'UP'
            else:
                return 'DOWN'
        elif self.direction == 'DOWN':
            if result == 1:
                return 'DOWN'
            elif result == 2:
                return 'RIGHT'
            else:
                return 'LEFT'
        else:
            if result == 1:
                return 'LEFT'
            elif result == 2:
                return 'DOWN'
            else:
                return 'UP'
            
    def draw_snake(self, environment, color, color_head):
        """Draws the snake on the environment

        Args:
            environment (object): Instance of class environment
            color (tuple): RGB values of color of snake
            color_head (tuple): RGB values of color of snake

        Returns:
            environment: Returns the environment after the snake has been drawn
        """
        l = self.unit
        for (x, y) in self.snake_position[1:]:
            draw.rect(environment, color, (x, y, l, l), 1)
            draw.rect(environment, color, (x+2, y+2, l-4, l-4))
        draw.rect(environment, color_head, (self.head_x, self.head_y, l, l), 1)
        draw.rect(environment, color_head,
                  (self.head_x+2, self.head_y+2, l-4, l-4))
        return environment