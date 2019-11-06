#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 23:42:07 2019

@author: ashay
"""

import pygame
import random
import time

pygame.init()

display_width=500
display_height=500
display= pygame.display.set_mode((display_width,display_height))
window_color=(200,200,200)
display.fill(window_color)
pygame.display.update()



clock=pygame.time.Clock()

button_direction=1

crashed=False

red=(255,0,0)
black=(0,0,0)

score=0

apple_image=pygame.image.load('apple.jpg')
snake_position=[[int(display_width/2),int(display_height/2)],[int(display_width/2-10),int(display_height/2)],[int(display_width/2-20),int(display_height/2)]]
snake_head=list(snake_position[0])

apple_position=[random.randrange(1,50)*10,random.randrange(1,50)*10]


print(snake_position)

def move(snake_position):
    global button_direction, apple_position,score
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            prev_button=button_direction
            if event.key == pygame.K_LEFT and prev_button !=1:
                button_direction=0
            elif event.key == pygame.K_RIGHT and prev_button !=0:
                button_direction=1
            elif event.key == pygame.K_UP and prev_button !=2:
                button_direction=3
            elif event.key == pygame.K_DOWN and prev_button !=3:
                button_direction=2
            else:
                button_direction=button_direction
          
    snake_head=list(snake_position[0])
    if button_direction==0:
        snake_head[0]-=10
    elif button_direction==1:
        snake_head[0]+=10
    elif button_direction==2:
        snake_head[1]+=10
    elif button_direction==3:
        snake_head[1]-=10
    else:
        pass
    
    
    snake_position.insert(0,snake_head)
    snake_position.pop()
    
    
    collision_with_apple(apple_position,snake_position,score)
        
    collision_with_boundaries(snake_position[0]) 
    collision_with_self(snake_position)
        
    
    

def display_snake(snake_position):
    display.fill(window_color)
    for position in snake_position:
        pygame.draw.rect(display,red,pygame.Rect(position[0],position[1],10,10))
        
def display_apple(display,apple_position,apple_image):
    display.blit(apple_image,(apple_position[0],apple_position[1]))

def collision_with_boundaries(snake_head):
    global crashed
    if snake_head[0]>=display_width or snake_head[0]<0 or snake_head[1]>=display_height or snake_head[1]<0:    
        print('collision_with_boundaries')
        crashed=True
        return 1
    else:
        return 0

def collision_with_self(snake_position):
    global crashed
    if snake_position[0] in snake_position[1:]:
        print('collision_with_self')
        crashed=True
        return 1
    else:
        return 0

def absorb_apple(apple_position,score,snake_position):
    print('absorb')
    score+=1
    apple_position=[random.randrange(1,50)*10,random.randrange(1,50)*10]
    while apple_position not in snake_position:
        apple_position=[random.randrange(1,50)*10,random.randrange(1,50)*10]
    return apple_position,score


def collision_with_apple(apple_position,snake_position,score):
    if snake_position[0]==apple_position:
        apple_position,score=absorb_apple(apple_position,score,snake_position)
        



if __name__ == "__main__":    
    
    while crashed is not True:    
        
        clock.tick(10)
        move(snake_position)
        display_snake(snake_position)
        display_apple(display,apple_position,apple_image)
        pygame.display.update()
    

    
    largeText=pygame.font.Font('freesansbold.ttf',30)
    TextSurf=largeText.render(str("Your final score is "+str(score)),True,black)
    TextRect=TextSurf.get_rect()
    TextRect.center=((display_width/2),(display_height/2))
    display.blit(TextSurf,TextRect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()