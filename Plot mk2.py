#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import libs
import numpy as np
import math
import matplotlib.pyplot as plt

#My Visual Studio doesn't support constructions like __name__=='__main__'
#I don't know why

def KapitzaPendulum(T, θ, dθ, ψ, A, L): #initialize a new function
    t = 0           #current time
    dt = 0.00001    #delta time

    ts = []         #the returned array of time
    θs = []         #the returned array of angles
    dθs = []        #the returned array of angle speed
    ddθs = []       #the returned array of angle acceleration

    while(t < T - dt):
        x = A * np.sin(ψ * t)  #положение подвеса
        ddθ = -(9.8 + ψ * ψ*x) * np.sin(θ)/L   #acceleration
        dθ += ddθ * dt      #velocity
        θ += dθ * dt        #angle
        t += dt
        ts.append(t)        #append element
        θs.append(θ)        #append element
        dθs.append(dθ)      #append element
        ddθs.append(ddθ)    #append element
    return (ts, θs, dθs, ddθs)  #return a tuple

KP = KapitzaPendulum(100, 3, 0, 100, 0.1, 2) #set the first graph

fig, axes = plt.subplots(4, 4)

#draw phase diagrams
for x in range(0, 4):
    for y in range(0, 4):
        axes[x, y].plot(KP[x], KP[y])  #get values from tuple

plt.show() #show the plot
