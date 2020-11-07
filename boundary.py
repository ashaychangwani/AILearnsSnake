import pygame
import random


class Playground:
    def __init__(self, height, width, block_size):
        self.height = height
        self.width = width
        self.block_size = block_size
        self.food = (0, 0)

    def create(self, playground, background_color, color):
        playground.fill(background_color)

        bs = self.block_size

        for w in range(0, self.width, bs):
            y = 0

            pygame.draw.rect(playground, color, (w, y, bs, bs), 1)
            pygame.draw.rect(playground, color, (w + 3, y+3, bs-6, bs-6))

            y = self.height - y

            pygame.draw.rect(playground, color, (w, y, bs, bs), 1)
            pygame.draw.rect(playground, color, (w+3, y+3, bs-6, bs-6))

        for h in range(0, self.height, bs):
            x = 0

            pygame.draw.rect(playground, color, (x, h, bs, bs), 1)
            pygame.draw.rect(playground, color, (x+3, h+3, bs-6, bs-6), 1)

            x = self.width - x

            pygame.draw.rect(playground, color, (x, h, bs, bs), 1)
            pygame.draw.rect(playground, color, (x+3, h+3, bs-6, bs-6))
        return playground

    def create_new_apple(self, snake_position):
        found = False
        bs = self.block_size
        while not found:
            x = random.randint( 2*bs, self.width -2*bs)
            x = x - (x%bs)
            y= random.randint( 2*bs, self.height -2*bs)
            y = y - (y%bs)
            
            i= 0 
            while i<len(snake_position):
                if x == snake_position[i][0] and y == snake_position[i][1]:
                    break
                i+=1
            if i == len(snake_position):
                found = True
                
        self.apple_position = (x, y)
        return self.apple_position

    def draw_apple(self, playground, color):
        pygame.draw.rect(playground, color, (self.apple_position[0], self.apple_position[1], self.block_size, self.block_size))
        return playground 

