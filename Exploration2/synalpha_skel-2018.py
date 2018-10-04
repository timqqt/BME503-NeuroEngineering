#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:45:08 2018

@author: chenriq
"""

from brian2 import *
defaultclock.dt=.0005*ms
duration = 100*ms
TAdt=0.001*ms
G=0*arange(0,duration/TAdt)
G[35000]=1.0 #time in timesteps that an event takes place 3500 is 3500*.01*ms or 35.0 ms
G[56000]=1.0
A1=TimedArray(G, dt=TAdt)
I=A1
vt = 1.*mV         # Spiking threshold
memc = 200.0*pfarad  # Membrane capacitance
bgcurrent = 200*pA   # External current
tau_m=2*ms
tau_ampa=2*ms
g_synpk=0.3*nsiemens
transwdth=1.0*ms


eqs_neurons='''
dv/dt=-v/tau_m + I(t)*mag : volt  #create a fake event to trigger a tspike
dg_ampa/dt = -g_ampa/tau_ampa : siemens # this is a exponential synapse

Trpre=.25*(tanh((t/ms-tspike/ms)/.005)-tanh((t/ms-(tspike/ms +transwdth/ms))/.005)):1

mag: volt/second
tspike:second
'''

# ###########################################
# Initialize neuron group
# ###########################################

neurons = NeuronGroup(1, model=eqs_neurons, clock=Clock(defaultclock.dt), threshold='v > vt',
                      reset='v=0*mV;g_ampa=g_synpk;tspike=t',refractory='0.3*ms',method="euler")

neurons.mag=1200.0*mV/ms
neurons.v=0.0*mV
neurons.tspike=-100.0*ms  #needed so a spike does not happen at time 0
# Comment these two lines out to see what happens without Synapses


M = StateMonitor(neurons, ('v','g_ampa','Trpre'), record=True)
sm = SpikeMonitor(neurons)

run(duration)
figure(1)
subplot(4,1,1) # plot of the fake voltage used to trigger a release
plot(M.t/ms, M.v[0]/mV, '-b')
xlim(0,duration/ms)
subplot(4,1,2) #plot of the conductance
plot(M.t/ms, M.g_ampa[0]/nsiemens, '-g', lw=2)
xlim(0,duration/ms)
subplot(4,1,3) #plot of the neurotransmitter release
plot(M.t/ms, M.Trpre[0], '-r', lw=2)
xlim(0,duration/ms)
subplot(4,1,4) # one way to plot the Timed Array Data in Brian
plot((arange(0,duration/ms,TAdt/ms)),I(arange(0,duration/ms,TAdt/ms)*ms))
xlim(0,duration/ms)
show()