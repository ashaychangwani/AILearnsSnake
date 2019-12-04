#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:19:50 2019

@author: ashay
"""

from keras.models import Sequential
from keras.layers import Dense,Dropout

def createModel(inpDim,weights):
    model=Sequential()
    model.add(Dense(inpDim,input_dim=inpDim,kernel_initializer='random_normal',activation='sigmoid'))
    model.add(Dense(int((inpDim+2)/2),kernel_initializer='random_normal',activation='sigmoid'))
    model.add(Dense(2,kernel_initializer='random_normal',activation='softmax'))
    model.compile(loss="categorical_crossentropy",optimizer='RMSProp',metrics=['accuracy'])
    model.set_weights(weights)
    return model


import numpy as np

def sigmoid(inpt):
    return 1.0 / (1.0 + numpy.exp(-1 * inpt))

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
    weights=flatten(weights)
    mat1=np.array(weights[0:inpDim*int((inpDim+3)/2)]).reshape((inpDim,int((inpDim+3)/2)))
    mat2=np.array(weights[inpDim*int((inpDim+3)/2):]).reshape(int((inpDim+3)/2),3)
    
    hiddenInput=np.matmul(inp,mat1)
    hiddenInput=sigmoid(hiddenInput)
    
    finalInput=np.matmul(hiddenInput,mat2)
    finalInput=softmax(finalInput)
    
    return list(finalInput).index(max(finalInput))
