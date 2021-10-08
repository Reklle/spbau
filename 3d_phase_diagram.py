#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import libs
import numpy as np
import math
import matplotlib.pyplot as plt

dt = 0.001      #delta time
t = 0           #current time
angl = 0.1      #inicoal angle
vlc = 0         #inicoal velocity
frec = np.pi*17 #frequency of oscillations
A = 0.1         #amplitude of oscillations
L = 1           #length

DATA = ([], [], [], [])     #t, θ, dθ, ddθ

#fig, axes = plt.subplots(4, 4)
T = 100
while(t < T):
    x = A * np.sin(frec * t)                   #положение подвеса
    accl = -(9.8 + frec * frec*x) * np.sin(angl)      #acceleration
    vlc += accl * dt      #velocity
    angl += vlc * dt      #angle
    t += dt               #increment of time
    if(t % 0.005 < dt):   #we don't need to append values to array every time in the cycle
        DATA[1].append(angl)     #append element
        DATA[2].append(vlc)      #append element
        DATA[3].append(accl)     #append element

#here we draw 3D phase diagram
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(DATA[1], DATA[2],  DATA[3], 'crimson')
ax.set_xlabel('Angle')          #Labels for axes
ax.set_ylabel('Velocity')       #Labels for axes
ax.set_zlabel('Acceleration')   #Labels for axes
plt.show()