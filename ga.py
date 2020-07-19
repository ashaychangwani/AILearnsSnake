#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:04:26 2019

@author: ashay
"""
from nn import *
import numpy as np
import bisect, collections,random
from main_game import *
import pygame
import matplotlib.pyplot as plt



'''
Inputs:
    FrontBlocked
    LeftBlocked
    RightBlocked
    GoalLeft
    GoalRight
    GoalFront
    GoalBack

Outputs:
    TurnLeft
    TurnRight
    GoForward
    
mid=int((inpNum+3)/2)           This is the neurons in the middle layer


 

NEW:
    Inputs:
        8 Directions:
            Distance to Wall
            Distance to Self
            Distance to apple
        (24 inputs so far)
        Angle of the apple wrt head of snake (range: 0-360)
        Distance of apple wrt head of snake
    Total 26 inputs
    
    Outputs:
        Turn left
        Turn Right
        Go Forward
'''

initPop=50
inpNum=26
mid=int((inpNum)/2)

mutationChance=0.95



def createInitPop(initPop=initPop):
    pop=list()
    for _ in range (initPop):
        temp=[]
        temp.append(np.resize(np.random.random(inpNum*mid) * 2 - 1,[inpNum,mid]))
        temp.append(np.resize(np.random.random(2*mid) * 2 - 1,[mid,3]))
        pop.append(temp)
    return pop
    
    
def cdf(weights):               #Cumulative distributive function
    total=sum(weights)
    result=[]
    cumsum=0
    for w in weights:
        cumsum+=w
        if total!=0:
            result.append(cumsum/total)
        else:
            result.append(0)
    return result


def choice(weights):                #A weighted version of random.choice
    cdf_vals=cdf(weights)
    x=random.random()
    idx=bisect.bisect(cdf_vals,x)
    return idx

def flatten(weights):
    return [item for sublist in weights for item in sublist.flatten()]

def crossOver(parent1, parent2):        
    flatParent1=flatten(parent1)
    flatParent2=flatten(parent2)
    crossOverPt=random.randint(0,(inpNum*mid + mid*3))
    #print('crossOverPoint',crossOverPt)
    temp=flatParent1[:crossOverPt] + flatParent2[crossOverPt:]
    flatParent2=flatParent2[:crossOverPt] + flatParent1[crossOverPt:]
    flatParent1=temp
    parent1=restructure(parent1,flatParent1)
    parent2=restructure(parent2,flatParent2)
    return parent1,parent2

def restructure(parent1,flatParent1):           #Basically anti-flatten 
    counter=0
    parent1[0]=np.array(flatParent1[:inpNum*mid]).reshape(inpNum,mid)
    counter=inpNum*mid
    parent1[1]=np.array(flatParent1[counter:]).reshape(mid,3)
    return parent1

def mutation(parent):
    mutationPt=random.randint(0,(inpNum*mid + mid*3 - 1))
    flatParent=flatten(parent)
    flatParent[mutationPt]=np.random.rand() * 2 - 1
    parent=restructure(parent,flatParent)
    return parent

def fitnessFn(chromosome):
    return playGameAI(chromosome)
 
    

def elitism(pop,fitness):
    global initPop
    t = list(zip(fitness,pop))
    #x for _,x in sorted(zip(fitness,pop))]
    t=sorted(t,key=lambda x: x[0])
    return [x for _,x in t[-1*int(initPop/10):]]
    

def offspringGeneration(pop):
    global children,maxVal,fitness,children
    fitness=list(np.zeros(initPop))
    pygame.init()
    maxVal=0
    for i in range (initPop):
        fitness[i]=0
        for _ in range(5):
            fitness[i]+=fitnessFn(pop[i])
        fitness[i]=int(fitness[i]/5)
        
    maxVal=max(fitness)
    
    
    fitness=[int(100*(x-min(fitness))/(max(fitness)-min(fitness)+1)) for x in fitness]
    children=list()
    children.extend(elitism(pop,fitness))
    #print('len(children)',len(children))
    while len(children)<initPop:
        t1=min(choice(fitness),49)
        t2=min(choice(fitness),49)
        #print('pop_size',len(pop),'t1',t1,'t2',t2)
        children.extend((crossOver(pop[t1],pop[t2])))
    for i in range (initPop):
        if random.random() >= mutationChance:
            children[i]=mutation(children[i])
    return children[:]
    

        
maxPerIteration=list()
fitness=None
pop=None
pop=createInitPop(initPop)
maxVal=0
for i in range(200):
    pop=offspringGeneration(pop)
    maxPerIteration.append(maxVal)
    print('Next iteration',maxPerIteration)
    if(maxVal<-600):
        pop=createInitPop(initPop)

    