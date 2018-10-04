#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 21:58:23 2018

@author: chenriq
"""

from brian2 import *
import numpy as np
Ox=np.load('outbugx.npy')
Oy=np.load('outbugy.npy')
srx=np.load('outsrx.npy')
sry=np.load('outsry.npy')
slx=np.load('outslx.npy')
sly=np.load('outsly.npy')
Ba=np.load('outbugang.npy')
Fx=np.load('outfoodx.npy')
Fy=np.load('outfoody.npy')
for i in range(0, len(Fy)):
           # Remove the last bug's position from the figure window
    bug_x_coords = [Ox[i], Ox[i]-4*cos(Ba[i]), Ox[i]-8*cos(Ba[i])]
    bug_y_coords = [Oy[i], Oy[i]-4*sin(Ba[i]), Oy[i]-8*sin(Ba[i])]
    bug_plot = plot(bug_x_coords, bug_y_coords, 'ko')    # Plot the bug's current position
    sr_plot = plot([Ox[i], srx[i]], [Oy[i], sry[i]], 'b')
    sl_plot = plot([Ox[i], slx[i]], [Oy[i], sly[i]], 'r')
    
    food_plot=plot(Fx[i], Fy[i], 'b*') 
    
    axis([-100,100,-100,100])
    draw()
    pause(0.02)
    bug_plot[0].remove()
    food_plot[0].remove()  
    sr_plot[0].remove()
    sl_plot[0].remove()
