#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:19:50 2019

@author: ashay
"""



import numpy as np

def sigmoid(inpt):
    return 1.0 / (1.0 + np.exp(-1 * inpt))

def softmax(x): 
    e_x = np.exp(x - np.max(x))     
    return e_x / e_x.sum(axis=0) 


def relu(inpt):
    result = inpt
    result[inpt < 0] = 0
    return result

def flatten(weights):
    return [item for sublist in weights for item in sublist.flatten()]

def getOutput(weights,inpDim,inp):
    mid = int((inpDim)/2)
    weights=flatten(weights)
    mat1=np.array(weights[0:inpDim*mid]).reshape(inpDim,mid)
    mat2=np.array(weights[inpDim*mid:]).reshape(mid,3)
    
    hiddenInput=np.matmul(inp,mat1)
    hiddenInput=sigmoid(hiddenInput)
    
    finalInput=np.matmul(hiddenInput,mat2)
    finalInput=sigmoid(finalInput)
    
    #print(list(finalInput).index(max(finalInput)))
    
    return list(finalInput).index(max(finalInput))