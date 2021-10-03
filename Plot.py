#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import libs
import numpy as np
import math
import matplotlib.pyplot as plt


def KapitzaPendulum(T, θ, dθ, ψ, A, L, sF):
    t = 0
    dt = 0.0001 #delta time
    ret = []    #the returned array
    while(t < T - dt):
        x = A * np.sin(ψ * t);  #положение подвеса
        ddθ = -(9.8 + ψ * ψ*x) * np.sin(θ)/L;   #acceleration
        dθ += ddθ * dt;     #velocity
        θ += dθ * dt;       #angle
        t += dt;
        ret.append(sF(θ, dθ, ddθ))  #append element
    return (np.arange(0, T, dt), ret)

#we initialize a function that selects one of three options for our graph: θ, dθ, ddθ
selectFunction = lambda x, y, z: x  #in this case, θ


KP = KapitzaPendulum(10, 3, 0, 300, 0.1, 2, selectFunction) #set the first graph
plt.plot(KP[0], KP[1])  #get (x, y) from tuple

KP = KapitzaPendulum(10, 3, 0, 100, 0.1, 2, selectFunction) #set the second graph
plt.plot(KP[0], KP[1])  #get (x, y) from tuple

plt.show() #show the plot