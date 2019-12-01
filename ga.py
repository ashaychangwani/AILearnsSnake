#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:04:26 2019

@author: ashay
"""
from nn import *
import numpy as np
import bisect, collections,random


initPop=50
inpNum=7
mid=int((inpNum+2)/2)

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

pop=list()
temp=list()


def createInitPop(initPop=initPop):
    for _ in range (initPop):
        temp=[]
        temp.append(np.resize(np.random.random(inpNum**2) * 2 - 1,[inpNum,inpNum]))
        temp.append(np.resize(np.zeros(mid),[inpNum]))
        temp.append(np.resize(np.random.random(inpNum*mid) * 2 - 1,[inpNum,mid]))
        temp.append(np.resize(np.zeros(mid),[mid]))
        temp.append(np.resize(np.random.random(2*mid) * 2 - 1,[mid,2]))
        temp.append(np.resize(np.array(np.zeros(2)),[2]))
        pop.append(temp)
        
        


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
    crossOverPt=random.randint(0,(inpNum**2 + inpNum*mid + mid*2 + inpNum + mid + 2))
    temp=flatParent1[:crossOverPt] + flatParent2[crossOverPt:]
    flatParent2=flatParent2[:crossOverPt] + flatParent1[crossOverPt:]
    flatParent1=temp
    parent1=restructure(parent1,flatParent1)
    parent2=restructure(parent2,flatParent2)
    return parent1,parent2

def restructure(parent1,flatParent1):
    counter=0
    parent1[0]=np.array(flatParent1[:inpNum**2]).reshape(inpNum,inpNum)
    counter=inpNum**2
    parent1[1]=np.array(flatParent1[counter : counter+inpNum]).reshape(inpNum,)
    counter=counter+inpNum
    parent1[2]=np.array(flatParent1[counter : counter + inpNum*mid]).reshape(inpNum,mid)
    counter=counter + inpNum*mid
    parent1[2]=np.array(flatParent1[counter : counter + mid]).reshape(mid,)
    counter=counter + mid
    parent1[4]=np.array(flatParent1[counter : counter + mid*2]).reshape(mid,2)
    counter = counter + mid*2
    parent1[5]=np.array(flatParent1[counter : counter + 2])
    return parent1
    


def mutation(parent):
    mutationPt=random.randint(0,(inpNum**2 + inpNum*mid + mid*2 + inpNum + mid + 2))
    if (np.random.rand() >= 0.80):
        flatParent=flatten(parent)
        if (flatParent[mutationPt] != 0.0):
            flatParent[mutationPt]=np.random.rand() * 2 - 1
            parent=restructure(parent,flatParent)
    return parent

zzz=[]

def fitnessFn(chromosome):
    global zzz
    model=createModel(inpNum,chromosome)
    print(model.predict(np.array(t).shape))
    

createInitPop(initPop)
fitnessFn(pop[0])




#(pop[0],pop[1])=crossOver(pop[0],pop[1])