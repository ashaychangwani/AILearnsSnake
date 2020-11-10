import pygame
import pickle
from snake import Environment, snake
from nn import NeuralNet
import time
import copy
from params import *



file = open('saved/test.pickle', "rb") 
snake_generations = pickle.load(file)
file.close()

best_snake = snake_generations[len(snake_generations)-1][0]
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
screen = pygame.display.set_mode((display_width, display_height))
environment = Environment(display_height, display_width, unit)
player = snake(display_width, display_height, NN_shape, unit, False)
player.neuralnet.theta = []
player.neuralnet.bias = []
player.neuralnet.setNextFood(
    environment.create_new_apple(player.snake_position))
screen = environment.create(screen, gray)
screen = environment.draw_apple(screen, pink)
screen = player.draw_snake(screen, blue, cherry)
pygame.display.update()

score = 0
decision = 0
while(player.isAlive()):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                decision = 2
            elif event.key == pygame.K_RIGHT:
                decision = 3
            elif event.key == pygame.K_DOWN:
                decision = 4
            else:
                decision = 1
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    if (player.head_x, player.head_y) == environment.apple_position:
        player.eatAppleHuman(decision)
        player.neuralnet.setNextFood(environment.create_new_apple(player.snake_position))
        score+=1
    


    player.moveHuman(decision)
    screen = environment.create(screen, gray)
    screen = environment.draw_apple(screen, pink)
    screen = player.draw_snake(screen, blue, cherry)
    prediction = player.convAIToDirections(best_snake.neuralnet.decision(
                player.head_x, player.head_y, player.snake_position, player.direction))

    pygame.display.set_caption('Score: '+str(score)+'\t\tAI recommends moving '+prediction)
    pygame.display.update()
    clock.tick(6)
 
pygame.display.update()       
largeText=pygame.font.Font('freesansbold.ttf',30)
TextSurf=largeText.render(str("Your final score is "+str(score)),True,pink)
TextRect=TextSurf.get_rect()
TextRect.center=((display_width/2),(display_height/2))
screen.blit(TextSurf,TextRect)
pygame.display.update()
time.sleep(2)
pygame.quit()