from pygame import draw
from neuralnet import NeuralNet
import random


class snake:
    def __init__(self, width, height, NN_shape, unit, init_NN=True, random_start=True):
        self.snake_position = []
        self.width = width
        self.height = height
        self.time_since_apple = 0
        self.collision_with_boundary = False
        self.collision_with_self = False
        self.unit = unit

        self.neuralnet = NeuralNet(
            NN_shape, self.width, self.height, self.unit, init_NN)

        self.snake_position.append(self.initSnake(random_start))

    def initSnake(self, random_start):
        if random_start:
            self.direction = random.choice(['RIGHT', 'UP', 'DOWN', 'LEFT'])
            self.head_x = random.randint(
                3,  self.width / self.unit - 3) * self.unit
            self.head_y = random.randint(
                3,  self.height / self.unit - 3) * self.unit
        else:
            self.direction = 'RIGHT'
            self.head_x, self.head_y = 40, 40
        return (self.head_x, self.head_y)

    def isAlive(self):
        if not self.collision_with_self and not self.collision_with_boundary:
            return True
        return False
    
    def eatApple(self, direction):
        self.snake_position.insert(0, (self.head_x, self.head_y))
        self.move(direction)

    def moveInDirection(self, direction):
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
        if self.head_x == self.unit or self.head_x == self.width - self.unit or self.head_y == self.unit or self.head_y == self.height - self.unit:
            self.collision_with_boundary = True
        for (body_x, body_y) in self.snake_position[1:]:
            if body_x == self.head_x and body_y == self.head_y:
                self.collision_with_self = True

    def move(self, result):
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

    def draw_snake(self, environment, color, color_head):
        l = self.unit
        draw.rect(environment, color_head, (self.head_x, self.head_y, l, l), 1)
        draw.rect(environment, color_head,
                  (self.head_x+2, self.head_y+2, l-4, l-4))
        for (x, y) in self.snake_position[1:]:
            draw.rect(environment, color, (x, y, l, l), 1)
            draw.rect(environment, color, (x+2, y+2, l-4, l-4))
        return environment