import pygame
import pickle
from snake import Environment, snake
from nn import NeuralNet
import time
import copy
from params import *

file = open('saved/model.pickle', "rb") 
snake_generations = pickle.load(file)
file.close()



pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
screen = pygame.display.set_mode((display_width, display_height))
environment = Environment(display_height, display_width, unit)
for i in range(len(snake_generations)):
    snakes = snake_generations[i]
    prev_score = -1
    for j in range(len(snakes)):
        saved_snake = snakes[j]
        pygame.display.set_caption('Generation : '+str(i+1)+'\t\tSnake Num: '+str(j+1)+'\t\tPrevious Score: '+str(prev_score))
        t_snake = snake(display_width, display_height, NN_shape, unit, False)
        t_snake.neuralnet.theta = saved_snake.neuralnet.theta
        t_snake.neuralnet.bias = saved_snake.neuralnet.bias
        t_snake.neuralnet.setNextFood(
            environment.create_new_apple(t_snake.snake_position))
        screen = environment.create(screen, gray)
        screen = environment.draw_apple(screen, pink)
        screen = t_snake.draw_snake(screen, blue, cherry)
        pygame.display.update()
        checkloop = False
        start_time = time.time()
        while t_snake.isAlive():
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    t_snake.collision_with_boundary = True
                    t_snake.collision_with_self = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            if (t_snake.head_x, t_snake.head_y) == environment.apple_position:
                t_snake.time_since_apple = 0
                result = t_snake.neuralnet.decision(t_snake.head_x, t_snake.head_y, t_snake.snake_position, t_snake.direction)
                t_snake.eatApple(result)
                t_snake.neuralnet.setNextFood(environment.create_new_apple(t_snake.snake_position))
                start_time = time.time()
                checkloop = False
                
            

            if t_snake.time_since_apple > 250:
                if not checkloop:
                    checkloop = True
                    any_point = (t_snake.head_x, t_snake.head_y)
                    times = 0
                elif (t_snake.head_x, t_snake.head_y) == any_point:
                    times += 1
                    if times > 4:
                        t_snake.collision_with_boundary = True
                        t_snake.collision_with_self = True
                        alive = False
            if time.time() - start_time > 7:
                t_snake.collision_with_boundary =  True
                t_snake.collision_with_self = True
                
            
            
            result = t_snake.neuralnet.decision(
                t_snake.head_x, t_snake.head_y, t_snake.snake_position, t_snake.direction)

            
            if not t_snake.move(result):
                prev_score = len(t_snake.snake_position) - 1
                
                    
                if t_snake.collision_with_boundary and t_snake.collision_with_self:
                    print('Generation: ' + str(i+1) + '\t\t' + \
                    'Snake Number: ' + str(j+1) + '\t\t' + \
                    'Score: ' + str(prev_score)+'\t\tReason: Stuck in Loop\t[Dead]')
                elif t_snake.collision_with_boundary:
                    print('Generation: ' + str(i+1) + '\t\t' + \
                    'Snake Number: ' + str(j+1) + '\t\t' + \
                    'Score: ' + str(prev_score)+'\t\tReason: Collision With Boundary\t[Dead]')
                else:
                    print('Generation: ' + str(i+1) + '\t\t' + \
                    'Snake Number: ' + str(j+1) + '\t\t' + \
                    'Score: ' + str(prev_score)+'\t\tReason: Collision With Self\t[Dead]')
                
            screen = environment.create(screen, gray)
            screen = environment.draw_apple(screen, pink)
            screen = t_snake.draw_snake(screen, blue, cherry)
            pygame.display.update()
        time.sleep(0.5)