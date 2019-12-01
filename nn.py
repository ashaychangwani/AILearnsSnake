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