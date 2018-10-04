#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 20:36:04 2018

@author: chenriq
"""

from brian2 import *
import numpy as np

map_size = 100
global foodx, foody, food_count, bug_plot, food_plot, sl_plot, sr_plot,outbugx,outbugy,outbugang,outfoodx,outfoody,outsrx,outsry,outslx,outsly
duration=100
outbugx=np.zeros(int(duration/2))
outbugy=np.zeros(int(duration/2))
outbugang=np.zeros(int(duration/2))
outfoodx=np.zeros(int(duration/2))
outfoody=np.zeros(int(duration/2))
outsrx=np.zeros(int(duration/2))
outsry=np.zeros(int(duration/2))
outslx=np.zeros(int(duration/2))
outsly=np.zeros(int(duration/2))

foodx = 50
foody = 50
food_count = 0

bug_eqs = '''
angle : 1
x : 1
y : 1
'''

bug = NeuronGroup(1, bug_eqs, clock=Clock(0.5*ms))
bug.x = 0
bug.y = 0
bug.angle = 0

sr_y_disp = 5   # y displacement of right sensor, relative to the bug's head
sr_x_disp = 5   # x displacement of right sensor
sl_y_disp = 5   # y displacement of left sensor
sl_x_disp = -5  # x displacement of left sensor

turn_rate = 1
base_speed = 0.025
speed_factor = 1

@network_operation()
def update():
    global foodx, foody, food_count, sr_x, sr_y, sl_x, sl_y
    sr_x = bug.x + sr_y_disp*cos(bug.angle) + sr_x_disp*sin(bug.angle)    # right sensor's x position
    sr_y = bug.y + sr_y_disp*sin(bug.angle) - sr_x_disp*cos(bug.angle)    # right sensor's y position

    sl_x = bug.x + sl_y_disp*cos(bug.angle) + sl_x_disp*sin(bug.angle)    # left sensor's x position
    sl_y = bug.y + sl_y_disp*sin(bug.angle) - sl_x_disp*cos(bug.angle)    # left sensor's y position

    if ((bug.x-foodx)**2+(bug.y-foody)**2) < 16:        # If the bug gets close enough to the food
        food_count += 1                                 # Count it
        foodx = randint(-map_size+10, map_size-10)      # Randomly place food somewhere else
        foody = randint(-map_size+10, map_size-10)

    if (bug.x < -map_size):                             # If the bug hits a wall
        bug.x = -map_size                               # "Bounce" off it
        bug.angle = pi - bug.angle
    if (bug.x > map_size):
        bug.x = map_size
        bug.angle = pi - bug.angle
    if (bug.y < -map_size):
        bug.y = -map_size
        bug.angle = -bug.angle
    if (bug.y > map_size):
        bug.y = map_size
        bug.angle = -bug.angle

    right_signal = 1/sqrt((foodx-sr_x)**2+(foody-sr_y)**2)      # Sensor signal inversely proportional to distance from food
    left_signal = 1/sqrt((foodx-sl_x)**2+(foody-sl_y)**2)

    dangle = turn_rate*(left_signal-right_signal)
    bug.angle = bug.angle + dangle

    speed = base_speed + speed_factor*(left_signal+right_signal)
    bug.x = bug.x + speed*cos(bug.angle)
    bug.y = bug.y + speed*sin(bug.angle)

@network_operation(dt=2*ms)
def update_plot(t):
    global foodx, foody, bug_plot, food_plot, sr_plot, sl_plot, sr_x, sr_y, sl_x, sl_y,outbugx,outbugy,outbugang,outfoodx,outfoody,outsrx,outsry,outslx,outsly
    indx=int(.5*t/ms+1)
    bug_plot[0].remove()        # Remove the last bug's position from the figure window
    food_plot[0].remove()       # Remove the last food position from the figure window
    sr_plot[0].remove()
    sl_plot[0].remove()
    bug_x_coords = [bug.x, bug.x-4*cos(bug.angle), bug.x-8*cos(bug.angle)]
    bug_y_coords = [bug.y, bug.y-4*sin(bug.angle), bug.y-8*sin(bug.angle)]
    outbugx[indx-1]=bug.x[0]
    outbugy[indx-1]=bug.y[0]
    outbugang[indx-1]=bug.angle[0]
    outfoodx[indx-1]=foodx
    outfoody[indx-1]=foody
    outsrx[indx-1]=sr_x
    outsry[indx-1]=sr_y
    outslx[indx-1]=sl_x
    outsly[indx-1]=sl_y
    bug_plot = plot(bug_x_coords, bug_y_coords, 'ko')     # Plot the bug's current position
    sr_plot = plot([bug.x, sr_x], [bug.y, sr_y], 'b')
    sl_plot = plot([bug.x, sl_x], [bug.y, sl_y], 'r')
    food_plot = plot(foodx, foody, 'b*')    # Plot the food's current position
    axis([-100,100,-100,100])
    draw()
    pause(0.1)    # Necessary for the plots to show up in real time


# Initialize plots
f = figure(1)
bug_plot = plot(bug.x, bug.y, 'wo')
food_plot = plot(foodx, foody, 'w*')
sr_plot = plot([bug.x[0],  5], [bug.y[0], 5], 'w')
sl_plot = plot([bug.x[0], -5], [bug.y[0], 5], 'w')


run(duration*ms,report='text')

np.save('outbugx',outbugx)
np.save('outbugy',outbugy)
np.save('outbugang',outbugang)
np.save('outfoodx',outfoodx)
np.save('outfoody',outfoody)
np.save('outsrx',outsrx)
np.save('outsry',outsry)
np.save('outslx',outslx)
np.save('outsly',outsly)