#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 23:42:07 2019

@author: ashay
"""

import pygame
import random
import time

from nn import *
    
def calcParams(snake_position,apple_position):
    '''
    FrontBlocked
    LeftBlocked
    RightBlocked
    GoalLeft
    GoalRight
    GoalFront
    GoalBack
    '''
    global button_direction
    param=[]
    head=snake_position[0]
    leftBlocked=rightBlocked=frontBlocked=0
    
    for i in snake_position[1:]:
        if i[1] == head[1]:
            if head[0]-i[0]==10:
                if button_direction==0: #Moving Left    1 means right
                    frontBlocked=1
                elif button_direction==2: #Moving Down
                    rightBlocked=1
                elif button_direction==3: #Moving Up
                    leftBlocked=1
            if i[0]-head[0]==10:
                if button_direction==1: 
                    frontBlocked=1
                elif button_direction==2:
                    leftBlocked=1
                elif button_direction==3:
                    rightBlocked=1
        if i[0] == head[0]:
            if head[1]-i[1] == 10:
                if button_direction==0: 
                    rightBlocked=1
                elif button_direction==1:
                    leftBlocked=1
                elif button_direction==3:
                    frontBlocked=1
            if i[1]-head[1] == 10:
                if button_direction==0: 
                    leftBlocked=1
                elif button_direction==1:
                    rightBlocked=1
                elif button_direction==2:
                    frontBlocked=1

    if head[0]==0:
        if button_direction==0: #Moving Left    1 means right
            frontBlocked=1
        elif button_direction==2: #Moving Down
            rightBlocked=1
        elif button_direction==3: #Moving Up
            leftBlocked=1
    if head[0]==display_width-10:
        if button_direction==1: 
            frontBlocked=1
        elif button_direction==2:
            leftBlocked=1
        elif button_direction==3:
            rightBlocked=1
    if head[1]==0:
        if button_direction==0: 
            rightBlocked=1
        elif button_direction==1:
            leftBlocked=1
        elif button_direction==3:
            frontBlocked=1
    if head[1]==display_height-10:
        if button_direction==0: 
            leftBlocked=1
        elif button_direction==1:
            rightBlocked=1
        elif button_direction==2:
            frontBlocked=1
    
    param.append(frontBlocked)
    param.append(leftBlocked)
    param.append(rightBlocked)

    xDiff=head[0]-apple_position[0]
    yDiff=head[1]-apple_position[1]
    
    
    goalRight=goalLeft=goalBack=goalFront=0
    
    if button_direction==0:     #Moving Left
        if(xDiff>0):
            goalFront=1
        elif(xDiff<0):
            goalBack=1
        if yDiff>0:
            goalRight=1
        elif yDiff<0:
            goalLeft=1
            
    elif button_direction==1:   #Moving Right
        if(xDiff>0):
            goalBack=1
        elif (xDiff<0):
            goalFront=1
        if yDiff>0:
            goalLeft=1
        elif yDiff<0:
            goalRight=1
        
    elif button_direction==2:   #Moving Down
        if(xDiff>0):
            goalRight=1
        elif (xDiff<0):
            goalLeft=1
        if yDiff>0:
            goalBack=1
        elif yDiff<0:
            goalFront=1
    elif button_direction==3:   #Moving Up
        if(xDiff>0):
            goalLeft=1
        elif(xDiff<0):
            goalRight=1
        if yDiff>0:
            goalFront=1
        elif yDiff<0:
            goalBack=1
            
    param.append(goalFront)
    param.append(goalBack)
    param.append(goalLeft)
    param.append(goalRight)
    
    return param


def move(snake_position):
    
    '''
    
    0 means LEFT
    1 means RIGHT
    3 means UP
    2 means DOWN
    
    '''
    
    global button_direction, apple_position,score,crashed
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
            break
        if event.type==pygame.QUIT:
            crashed=True
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
    absorbedApple=collision_with_apple(snake_position)
    snake_position.insert(0,snake_head)
    if not absorbedApple:
        snake_position.pop()
        

    
    #print(snake_position)    
    collision_with_boundaries(snake_position[0]) 
    collision_with_self(snake_position)
    
    
def move2(snake_position,decision):
         
    '''
    
    0 means LEFT
    1 means RIGHT
    3 means UP
    2 means DOWN
    
    
    
    outputs: 
        
        0 means left
        1 means straight 
        2 means right
    '''
    
    global button_direction, apple_position,score,crashed,counterSinceApple
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            crashed=True
            
    prev_button=button_direction
    if decision == 0:
        if prev_button == 0:
            button_direction = 2
        elif prev_button == 1:
            button_direction = 3
        elif prev_button == 2:
            button_direction = 1
        elif prev_button == 3:
            button_direction = 0
    elif decision == 1:
        button_direction=prev_button
    elif decision == 2:
        if prev_button == 0:
            button_direction = 3
        elif prev_button == 1:
            button_direction = 2
        elif prev_button == 2:
            button_direction = 0
        elif prev_button == 3:
            button_direction = 1

    
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
    absorbedApple=collision_with_apple(snake_position)
    snake_position.insert(0,snake_head)
    if not absorbedApple:
        snake_position.pop()

    counterSinceApple+=1
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
        #print('collision_with_boundaries')
        crashed=True
        return 1
    else:
        return 0

def collision_with_self(snake_position):
    global crashed
    if snake_position[0] in snake_position[1:]:
        #print('collision_with_self')
        crashed=True
        return 1
    else:
        return 0



def collision_with_apple(snake_position):
    global apple_position,score,counterSinceApple
    if snake_position[0]==apple_position:
        score+=200
        apple_position=[random.randrange(1,49)*10,random.randrange(1,49)*10]
        counterSinceApple=0
        while apple_position in snake_position:
            apple_position=[random.randrange(1,50)*10,random.randrange(1,50)*10]
        return True
        

def playGame():
    global score,crashed,snake_position,apple_position, display, apple_image
    
    while crashed is not True:    
        
        #clock.tick()
        clock.tick(40)
        time.sleep(0.2)
        move(snake_position)
        
        param=calcParams(snake_position, apple_position)
        
        #print(snake_position,'\nFrontBlocked\t',param[0],'\nLeftBlocked\t',param[1],'\nRightBlocked\t',param[2],'\nGoalFront\t',param[3],'\nGoalBack\t',param[4],'\nGoalLeft\t',param[5],'\nGoalRight\t',param[6])
    
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
    return score


def playGameAI(weights):
    global score,crashed,snake_position,apple_position, display, apple_image, counterSinceApple
    init()
    while crashed is not True and counterSinceApple <= 1000:    
        
        clock.tick()
        #clock.tick(40)
        
        param=calcParams(snake_position, apple_position)
        #print(snake_position,'\nFrontBlocked\t',param[0],'\nLeftBlocked\t',param[1],'\nRightBlocked\t',param[2],'\nGoalFront\t',param[3],'\nGoalBack\t',param[4],'\nGoalLeft\t',param[5],'\nGoalRight\t',param[6])
    
        if param[3]==1:
            score-=1
        else:
            score-=2
        move2(snake_position,getOutput(weights,7,param))
        
        
        display_snake(snake_position)
        display_apple(display,apple_position,apple_image)
        
        pygame.display.update()
    

    
    largeText=pygame.font.Font('freesansbold.ttf',30)
    TextSurf=largeText.render(str("Your final score is "+str(score)),True,black)
    TextRect=TextSurf.get_rect()
    TextRect.center=((display_width/2),(display_height/2))
    display.blit(TextSurf,TextRect)
    pygame.display.update()
    #time.sleep(2)
    #pygame.quit()
    #print(score)
    return score



def init():
    global crashed,counterSinceApple,button_direction,score,param,snake_position,snake_head,apple_position
    counterSinceApple=0
    crashed=False
    button_direction=0
    score=0
    param=[]
    snake_position=[[int(display_width/2),int(display_height/2)],[int(display_width/2+10),int(display_height/2)],[int(display_width/2+20),int(display_height/2)],[int(display_width/2+30),int(display_height/2)],[int(display_width/2+40),int(display_height/2)]]
    snake_head=list(snake_position[0])
    
    apple_position=[random.randrange(1,50)*10,random.randrange(1,50)*10]
    

#pygame.init() #UNCOMMENT THIS TO TRY MANUAL GAME
display_width=500
display_height=500
display=pygame.display.set_mode((display_width,display_height))
window_color=(200,200,200)
display.fill(window_color)
pygame.display.update()



clock=pygame.time.Clock()



red=(255,0,0)
black=(0,0,0)


apple_image=pygame.image.load('apple.png')
apple_image=pygame.transform.scale(apple_image,(10,10))
    
if __name__ == '__main__':
    
    init()    
    pygame.init()
    #Score=playGameAI(pop[0])
    score=playGame() 
    print(score)
