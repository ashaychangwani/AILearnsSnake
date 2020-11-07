import pygame
import pickle
from boundary import Playground
from snake import *
import time

width = 540
height = 440
block_size = 20
layers = [24, 16, 3]
random_params = True
population_size = 50
no_of_generations = 30
per_of_best_old_pop = 20.0  # percent of best performing parents to be included
per_of_worst_old_pop = 2.0  # percent of worst performing parents to be included
mutation_percent = 7.0
mutation_intensity = 0.1

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
light_red = (150, 0, 0)
blue = (106, 133, 164)
pink = (171, 54, 81)
lavender = (230, 230, 250)
gray = (55, 55, 55)
bg = (170, 202, 154)

file = open('saved/test.pickle', "rb")
snakes = pickle.load(file)

generation = 29

file.close()

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Generation : 0\t\tScore : 0')
seed = random.random()
playground = Playground(height, width, block_size)

for saved_snake in snakes:
    t_snake = snake(width, height, layers, block_size, False)

    t_snake.neuralnet.weights = saved_snake.neuralnet.weights
    t_snake.neuralnet.bias = saved_snake.neuralnet.bias
    random.seed(seed)
    t_snake.neuralnet.setNextFood(
        playground.create_new_apple(t_snake.snake_position))
    screen = playground.create(screen, bg, gray)
    screen = playground.draw_apple(screen, pink)
    screen = t_snake.draw_snake(screen, blue)
    pygame.display.update()
    checkloop = False
    while t_snake.isAlive():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pressed = True
                while pressed:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                            pressed = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                t_snake.collision_with_boundary = True
                t_snake.collision_with_self = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        result = t_snake.neuralnet.decision(
            t_snake.head_x, t_snake.head_y, t_snake.snake_position, t_snake.direction)

        alive = t_snake.move(result)

        if t_snake.steps_taken > (len(t_snake.snake_position)/5*100):
            if not checkloop:
                checkloop = True
                any_point = (t_snake.head_x, t_snake.head_y)
                times = 0
            if (t_snake.head_x, t_snake.head_y) == any_point:
                times += 1
            if times > 4:
                t_snake.collision_with_boundary = True
                t_snake.collision_with_self = True
                alive = False
        else:
            checkloop = False
        if not alive:
            text = 'Generation : ' + str(generation+1) + '\t\t' + \
                'Score : ' + str(len(t_snake.snake_position)-1)+'\t[Dead]'
            if t_snake.collision_with_boundary and t_snake.collision_with_self:
                print('killed,', 'generation : ',
                      generation+1, 'score : ', len(t_snake.snake_position)-1)
            elif t_snake.collision_with_boundary and not t_snake.collision_with_self:
                print('crashed on wall,', 'generation : ',
                      generation+1, 'score : ', len(t_snake.snake_position)-1)
            else:
                print('crashed on body,', 'generation : ',
                      generation+1, 'score : ', len(t_snake.snake_position)-1)
            pygame.display.set_caption(text)
            time.sleep(0.)
            break
        if (t_snake.head_x, t_snake.head_y) == playground.food:
            t_snake.steps_taken = 0
            next_position = t_snake.neuralnet.decision(
                t_snake.head_x, t_snake.head_y, t_snake.snake_position, t_snake.direction
            )
            if not t_snake.updateSnakePosition(next_position):
                t_snake.collision_with_boundary = True
            t_snake.neuralnet.setNextFood(playground.create_new_apple(t_snake.snake_position))
        screen = playground.create(screen, bg, gray)
        screen = playground.draw_apple(screen, pink)
        screen = t_snake.draw_snake(screen, blue)
        pygame.display.update()
        
        text = 'Generation : ' + str(generation+1) + '\t\t' + \
                'Score : ' + str(len(t_snake.snake_position)-1)+'\t[Press q to kill]'
        
