#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 23:42:07 2019

@author: ashay
"""

import pygame
import random
import time
import math

from math import degrees, atan2

from nn import *
    
inpNum=26



def distanceBetweenPoints(x1,y1,x2,y2):
    '''
    Euclidean Distance Between Two Points
    '''
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist  
    
    
def bodyCollision(snake_head, snake_position, deltaX, deltaY):
    minDist=10000000
    for pos in snake_position[1:]:
        x=pos[0]-snake_head[0]
        y=pos[1]-snake_head[1]
        #print(pos,x,y)
        
        if (deltaX==0 or (x % deltaX==0 and x/deltaX>0)) and (deltaY==0 or (y % deltaY == 0 and y/deltaY>0)):
            minDist=min(minDist,distanceBetweenPoints(pos[0],pos[1],snake_head[0],snake_head[1]))
                
        #print(minDist)
        '''
        
        needs work because should have different results because imagine that delta=10 and diff=-100
    
        '''
    if(minDist==10000000):
        return -1
    return minDist/display_width


def AngleBtw2Points(pointA, pointB):
      changeInX = pointB[0] - pointA[0]
      changeInY = pointB[1] - pointA[1]
      return degrees(atan2(changeInY,changeInX))/180 #remove degrees if you want your answer in radians


def appleCollision(snake_head, apple_position, deltaX, deltaY):
    x=apple_position[0]-snake_head[0]
    y=apple_position[1]-snake_head[1]
    
    if (deltaX==0 or (x % deltaX==0 and x/deltaX>0)) and (deltaY==0 or (y % deltaY == 0 and y/deltaY>0)):
        return distanceBetweenPoints(snake_head[0], snake_head[1], apple_position[0], apple_position[1])/(diag)
    
    
    return -1;
        
    
    
    '''
    
    currently just checking +10 -10 etc. 
    
    have to edit to ensure to check in that direction, so have to use division and check if division = delta
    
    '''
    
    



def calcNewParams(snake_position, apple_position):
    global crashed
    '''
    

    Parameters
    ----------
    snake_position : TYPE
        DESCRIPTION.
    apple_position : TYPE
        DESCRIPTION.



    Calculates
    ----------
    
    Distance from Top 
    Distance from 45 deg wall
    Distance from Right Wall
    Distance from bottom right wall
    Distance from bottom wall
    Distance from bottom left wall
    Distance from left wall
    Distance from top left wall
    
    8 more distances from self in that direction
    
    Distance from apple
    Direction of apple
    
    
    Total 18 inputs
    
    
        actually total is 26
    
    Returns
    -------
    parameters

    '''
    
    param=[]
    
    snake_head=snake_position[0]
    x=snake_head[0]
    y=snake_head[1]
    
    '''
    
    range 0 to 490
    
    '''
    
    
    param.append(y)
    
    param.append(min(distanceBetweenPoints(x, y, x+y, 0), distanceBetweenPoints(x, y, display_width-10, y - (display_width-10-x))))     #Find which wall it hits first, top wall or right wall
    
    param.append(display_width-10-x)
    
    param.append(min(distanceBetweenPoints(x, y, display_width-10, y+(display_width-10-x)),distanceBetweenPoints(x, y, x+(display_width-10-y), display_width-10)))
    
    param.append(display_width-10-y)
    
    param.append(min(distanceBetweenPoints(x, y, 0, x+y), distanceBetweenPoints(x, y, x-(display_width-10-y), display_width-10)))
    
    param.append(x)
    
    param.append(min(distanceBetweenPoints(x, y, x-y, 0),distanceBetweenPoints(x, y, 0, y-x)))
    
    param=[(i/(diag/2))-1 for i in param]
    
    '''
    
    Now to add the 8 body collision ones
    
    range -1 to 1 (-1 for no collision, 0 to 1 to for other ranges, by dividing by 500)
    
    '''
    
    
    param.append(bodyCollision(snake_head, snake_position, 0,-10))
    
    param.append(bodyCollision(snake_head, snake_position, 10,-10))
    
    param.append(bodyCollision(snake_head, snake_position, 10,0))
    
    param.append(bodyCollision(snake_head, snake_position, 10,10))
    
    param.append(bodyCollision(snake_head, snake_position, 0,10))
    
    param.append(bodyCollision(snake_head, snake_position, -10,10))
    
    param.append(bodyCollision(snake_head, snake_position, -10,0))
    
    param.append(bodyCollision(snake_head, snake_position, -10,-10))
    
    
    '''
    Now adding the 8 apple distance ones
    
    range -1 to 1
    '''
    
    
    param.append(appleCollision(snake_head, apple_position, 0,-10))
    
    param.append(appleCollision(snake_head, apple_position, 10,-10))
    
    param.append(appleCollision(snake_head, apple_position, 10,0))
    
    param.append(appleCollision(snake_head, apple_position, 10,10))
    
    param.append(appleCollision(snake_head, apple_position, 0,10))
    
    param.append(appleCollision(snake_head, apple_position, -10,10))
    
    param.append(appleCollision(snake_head, apple_position, -10,0))
    
    param.append(appleCollision(snake_head, apple_position, -10,-10))
    
    
    
    
    
    '''
    Now adding the euclidean distance, and then the angle
    
    scale -1 to 1
    '''

    param.append((distanceBetweenPoints(snake_head[0], snake_head[1], apple_position[0],apple_position[1])/(diag/2))-1) 
    
    param.append(AngleBtw2Points(snake_head, apple_position))
    
    
    
    
    for i in param:
        if i>1:
            print(param)
        elif i<-1:
            print(param)
    
    return param
    
    
    
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


def move(snake_position):       #Move for User Program
    
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
            #pygame.display.quit()
            pygame.quit()
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
    
    collision_with_boundaries(snake_position[0]) 
    collision_with_self(snake_position)
    
    absorbedApple=collision_with_apple(snake_position)
    snake_position.insert(0,snake_head)
    if not absorbedApple:
        snake_position.pop()
        

    
    #print(snake_position)    
    
    
def move2(snake_position,decision):     ##fuction for moving snake according to AI prediction
         
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
            #pygame.display.quit()
            pygame.quit()
            
    prev_button=button_direction
    
    
    
    
    if decision == 0:           #This entire block is to account for relative movement WRT head direction
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
    global crashed,score,anyAppleEaten
    if snake_head[0]>=display_width or snake_head[0]<0 or snake_head[1]>=display_height or snake_head[1]<0:    
        #print('collision_with_boundaries')
        crashed=True
        score-=150
        if not anyAppleEaten:
            score-=500
        return 1
    else:
        return 0

def collision_with_self(snake_position):
    global crashed,score,anyAppleEaten
    if snake_position[0] in snake_position[1:]:
        #print('collision_with_self')
        crashed=True
        score-=150
        if not anyAppleEaten:
            score-=500
        return 1
    else:
        return 0

def collision_with_apple(snake_position):
    global apple_position,score,counterSinceApple,anyAppleEaten
    if snake_position[0]==apple_position:
        score+=500
        apple_position=[random.randrange(1,49)*10,random.randrange(1,49)*10]
        counterSinceApple=0
        anyAppleEaten=True
        while apple_position in snake_position:
            apple_position=[random.randrange(1,50)*10,random.randrange(1,50)*10]
        return True
        

def playGame():
    global score,crashed,snake_position,apple_position, display, apple_image
    
    while crashed is not True:    
        
        display_snake(snake_position)
        display_apple(display,apple_position,apple_image)
        #clock.tick()
        clock.tick(40)
        time.sleep(0.2)
        
        #time.sleep(4)
        move(snake_position)
        param=calcNewParams(snake_position, apple_position)
        #print(snake_position,'\nFrontBlocked\t',param[0],'\nLeftBlocked\t',param[1],'\nRightBlocked\t',param[2],'\nGoalFront\t',param[3],'\nGoalBack\t',param[4],'\nGoalLeft\t',param[5],'\nGoalRight\t',param[6])
    
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
    global score,crashed,snake_position,apple_position, display, apple_image, counterSinceApple,anyAppleEaten
    init()
    oldDistance=diag
    while crashed is not True and counterSinceApple <= 1000:    
        
        clock.tick()
        #clock.tick(40)
        
        param=calcNewParams(snake_position, apple_position)
        
        
        '''
        if param[3]==1:
            score-=1
        else:
            score-=2
        '''
        if(oldDistance>param[24]):
            score+=2
        else:
            score-=1
        oldDistance=param[24]
        move2(snake_position,getOutput(weights,inpNum,param))
        
        
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
    global crashed,counterSinceApple,button_direction,score,param,snake_position,snake_head,apple_position,anyAppleEaten
    counterSinceApple=0
    crashed=False
    anyAppleEaten=False
    button_direction=0
    score=0
    param=[]
    snake_position=[[int(display_width/2),int(display_height/2)],[int(display_width/2+10),int(display_height/2)],[int(display_width/2+20),int(display_height/2)],[int(display_width/2+30),int(display_height/2)],[int(display_width/2+40),int(display_height/2)]]
    snake_head=list(snake_position[0])
    
    apple_position=[random.randrange(1,50)*10,random.randrange(1,50)*10]
    

display_width=500
display_height=500
display=pygame.display.set_mode((display_width,display_height))
window_color=(200,200,200)
display.fill(window_color)
pygame.display.update()


diag=math.sqrt(2)* display_width

clock=pygame.time.Clock()



red=(255,0,0)
black=(0,0,0)


apple_image=pygame.image.load('apple.png')
apple_image=pygame.transform.scale(apple_image,(10,10))
    
if __name__ == '__main__':
    
    init()    
    pygame.init()
    score=playGame() 
    print(score)