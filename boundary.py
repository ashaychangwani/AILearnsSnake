import pygame
import random


class Environment:
    def __init__(self, height, width, unit_size):
        self.height = height
        self.width = width
        self.unit = unit_size
        self.apple_position = (0, 0)

    def draw_apple(self, environment, color):
        apple_image = pygame.image.load('apple.png')
        apple_image = pygame.transform.scale(apple_image, (10, 10))
        environment.blit(
            apple_image, (self.apple_position[0], self.apple_position[1], self.unit, self.unit))
        return environment

    def draw_boundary(self, environment, color):
        unit = self.unit
        for w in range(0, self.width, self.unit):
            pygame.draw.rect(environment, color, (w, 0, unit, unit))
            pygame.draw.rect(environment, color,
                             (w, self.height - unit, unit, unit))
        for h in range(0, self.height, self.unit):
            pygame.draw.rect(environment, color, (0, h, unit, unit))
            pygame.draw.rect(environment, color,
                             (self.width - unit, h, unit, unit))

    def create(self, environment, color):
        environment.fill((200, 200, 200))
        self.draw_boundary(environment, color)
        return environment

    def create_new_apple(self, snake_position):
        unit = self.unit
        apple_position = (unit*random.randint(2, self.width/unit - 2),
                          unit*random.randint(2, self.height/unit - 2))
        while any(body == apple_position for body in snake_position):
            apple_position = (unit*random.randint(2, self.width/unit - 2),
                              unit*random.randint(2, self.height/unit - 2))
        self.apple_position = apple_position
        return self.apple_position
