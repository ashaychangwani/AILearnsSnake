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
'''

initPop=100
inpNum=7
mid=int((inpNum+3)/2)



def createInitPop(initPop=initPop):
    global fitness,parentFitnessSum,maxVal
    fitness=list(numpy.arange(initPop))
    pop=list()
    for _ in range (initPop):
        temp=[]
        temp.append(np.resize(np.random.random(inpNum*mid) * 2 - 1,[inpNum,mid]))
        temp.append(np.resize(np.random.random(3*mid) * 2 - 1,[mid,3]))
        pop.append(temp)
    
    for i in range (initPop):
        fitness[i]=fitnessFn(pop[i])
    parentFitnessSum=sum(fitness)
    maxVal=max(fitness)
    fitness=[x+min(fitness) for x in fitness]
    return pop
    
    
def cdf(weights):
    total=sum(weights)
    result=[]
    cumsum=0
    for w in weights:
        cumsum+=w
        result.append(cumsum/total)
    return result


def choice(weights):
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

def restructure(parent1,flatParent1):
    counter=0
    parent1[0]=np.array(flatParent1[:inpNum*mid]).reshape(inpNum,mid)
    counter=inpNum*mid
    parent1[1]=np.array(flatParent1[counter:]).reshape(mid,3)
    return parent1

def mutation(parent):
    mutationPt=random.randint(0,(inpNum*mid + mid*3 - 1))
    if (np.random.rand() >= 0.80):
        flatParent=flatten(parent)
        if (flatParent[mutationPt] != 0.0):
            flatParent[mutationPt]=np.random.rand() * 2 - 1
            parent=restructure(parent,flatParent)
    return parent

def fitnessFn(chromosome):
    return playGameAI(chromosome)
 

def elitism(pop,fitness):
    global initPop,parentFitnessSum
    t = list(zip(fitness,pop))
    #x for _,x in sorted(zip(fitness,pop))]
    t=sorted(t,key=lambda x: x[0])
    return [x for _,x in t[-1*int(initPop/25):]]
    

def offspringGeneration(pop):
    global children,maxVal,fitness,children,parentFitnessSum
    
    fitness=list(numpy.arange(initPop))
    pygame.init()
    maxVal=0
    children=list()
    children.extend(elitism(pop,fitness))
    while len(children)<initPop:
        t1=choice(fitness)
        t2=choice(fitness)
        children.extend((crossOver(pop[t1],pop[t2])))
    for i in range (initPop):
        if random.random() >= 0.98:
            children[i]=mutation(children[i])
        fitness[i]=fitnessFn(children[i])
    childFitnessSum=sum(fitness)
    maxVal=max(fitness)
    fitness=[x+min(fitness) for x in fitness]
    if childFitnessSum>=parentFitnessSum:
        parentFitnessSum=childFitnessSum
        return children[:]
    else:
        pop2=list()
        pop2.extend(elitism(children,fitness))
        for i in range (initPop):
            fitness[i]=fitnessFn(pop[i])
        while len(pop2)<initPop:
            t1=choice(fitness)
            t2=choice(fitness)
            pop2.extend((crossOver(pop[t1],pop[t2])))
        for i in range (initPop):
            if random.random() >= 0.98:
                pop2[i]=mutation(pop2[i])
            fitness[i]=fitnessFn(pop2[i])
        parentFitnessSum=sum(fitness)
        maxVal=max(fitness)
        fitness=[x+min(fitness) for x in fitness]
        return pop2[:]
        
    

        
maxPerIteration=list()
fitness=None
pop=None
pop=createInitPop(initPop)
maxVal=0
while maxVal < 10000:
    pop=offspringGeneration(pop)
    maxPerIteration.append(maxVal)
    print('Next iteration\n',maxPerIteration)