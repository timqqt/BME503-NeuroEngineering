#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:45:08 2018

@author: chenriq
"""

from brian2 import *
defaultclock.dt=.0100*ms
# Time setting for NMDA
# duration = 1800*ms
# TAdt = 0.001*ms
# G=0*arange(0, duration/TAdt)
# G[200000] = 1.0 #time in timesteps that an event takes place 3500 is 3500*.01*ms or 35.0 ms
# G[1200000] = 1.0
duration = 2400*ms
TAdt=0.001*ms
G=0*arange(0,duration/TAdt)
G[200000] = 1.0 #time in timesteps that an event takes place 3500 is 3500*.01*ms or 35.0 ms
G[1400000] = 1.0
A1 = TimedArray(G, dt=TAdt)
I = A1
vt = 1.*mV         # Spiking threshold
memc = 200.0*pfarad  # Membrane capacitance
bgcurrent = 200*pA   # External current
# AMPA 5*ms , NMDA 200*ms GABAa 7*ms
tau_m = 200*ms
# tau_ampa=2*ms
# AMPA 0.1 NMDA 0.096 GABAa 0.26 GABAb
g_synpk=0.00054*siemens
transwdth=1.0*ms
# parameters for post-synaptic
T_max = 1*mM
VT = 2*mV
Kp = 5*mV
# AMPA
g_ampa_m = 0.25*siemens
E_ampa = 0*mV
alpha_ampa = 1.1/ms # due to T's unit is 1
beta_ampa = 0.19/ms
# NMDA
g_nmda_m = 2.5*siemens
E_nmda = 0*mV
alpha_nmda = 0.072/ms # due to T's unit is 1
beta_nmda = 0.0066/ms
# GABAa
g_gaba_a_m = 0.3*siemens
E_gabaa = -75*mV
alpha_gabaa = 5.0/ms # due to T's unit is 1
beta_gabaa = 0.18/ms
# GABAb
g_gaba_b_m = 0.3*siemens
E_K = -90*mV
alpha_gabab = 0.09/ms # due to T's unit is 1
beta_gabab = 0.0012/ms
K_3 = 0.18/ms
K_4 = 0.034/ms
K_d = 100
# Equations
# eqs_AMPA='''
# I_ampa = g_ampa_m*s_1*(v-E_ampa) : amp
# ds_1/dt = alpha_ampa*Trpre*(1-s_1)-beta_ampa*s_1 : 1
# g_ampa = g_ampa_m*s_1 : siemens
# '''
# eqs_NMDA='''
# I_nmda = g_nmda*Bv*s_2*(v-E_nmda) : amp
# ds_2/dt = alpha_nmda*Trpre*(1-s_2)-beta_nmda*s_2 : 1
# g_nmda = g_nmda_m*s_2*Bv : siemens
# Bv = 1 : 1
# '''
# eqs_GABAa='''
# I_gaba_a = g_gaba_a_m*s_3*(v-E_gabaa) : amp
# ds_3/dt = alpha_gabaa*Trpre*(1-s_3)-beta_gabaa*s_3 : 1
# g_gaba_a = g_gaba_a_m * s_3 : siemens
# '''
eqs_GABAb='''
I_gaba_b = g_gaba_b_m*(s**4/(s**4+K_d))*(v-E_K) : amp
ds/dt = K_3*r-K_4*s : 1
dr/dt = alpha_gabab*Trpre*(1-r)-beta_gabab*r : 1
g_gaba_b =g_gaba_b_m*((s**4)/((s**4)+K_d)) : siemens
'''
eqs_neurons='''
dv/dt=-v/tau_m + I(t)*mag : volt  #create a fake event to trigger a tspike
# dg_ampa/dt = -g_ampa/tau_ampa : siemens # this is a exponential synapse
Trpre=.25*(tanh((t/ms-tspike/ms)/.005)-tanh((t/ms-(tspike/ms +transwdth/ms))/.005)):1

# The conductance of the alpha model
dz/dt = (-z/tau_m) : siemens
# do not need this for one time constant model + (g_synpk/(tau_m*exp(-1))) * (I(t)*mag/(mV/ms))
dg/dt = -g/tau_m + z/ms : siemens

mag: volt/second
tspike:second
'''

eqs_neurons += eqs_GABAb
# ###########################################
# Initialize neuron group
# ###########################################

neurons = NeuronGroup(1, model=eqs_neurons, clock=Clock(defaultclock.dt), threshold='v > vt',
                      reset='v=0*mV;g = g_synpk;r = 0.1;s = 0.01;tspike=t', refractory='0.5*ms', method="euler")

neurons.mag = 2400.0*mV/ms
neurons.v = 0.0*mV
neurons.tspike = -100.0*ms  #needed so a spike does not happen at time 0
# Comment these two lines out to see what happens without Synapses


M = StateMonitor(neurons, ('v', 'g_gaba_b', 'Trpre', 'g'), record=True)
sm = SpikeMonitor(neurons)

run(duration)
figure(1)
# subplot(4, 1, 1) # plot of the fake voltage used to trigger a release
# plot(M.t/ms, M.v[0]/mV, '-b')
# xlim(0, duration/ms)
# title('NMDA synapses')
# subplot(4, 1, 2) #plot of the conductance
plot(M.t/ms, M.g_gaba_b[0]/siemens, '-g', lw=2)
print(M.g_gaba_b[0]/siemens)
plot(M.t/ms, M.g[0]/siemens, color='black', lw=2)

xlim(0, duration/ms)
ylim(-0.0001, 0.0008)
title('GABAb synapses')
# subplot(4, 1, 3) #plot of the neurotransmitter release
# plot(M.t/ms, M.Trpre[0], '-r', lw=2)
# xlim(0, duration/ms)
# subplot(4, 1, 4) # one way to plot the Timed Array Data in Brian
# plot((arange(0, duration/ms, TAdt/ms)), I(arange(0, duration/ms, TAdt/ms)*ms))
# xlim(0, duration/ms)
show()
import matplotlib.pyplot as plt

plt.hist()