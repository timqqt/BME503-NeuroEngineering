#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:38:19 2018

@author: chenriq
"""
from brian2 import *
import random
import numpy as np 
import matplotlib.pyplot as plt

  

duration=1500*ms
div=0.01*ms
stimlist=numpy.zeros(1500)
pulselist=numpy.arange(10,500,40)
stimlist[pulselist]=1 
pulselist2=numpy.arange(1000,1500,40)
stimlist[pulselist2]=1    

#duration = .02*second

A1=TimedArray(stimlist*mV/mV,dt=.001*second)
I1=A1

stimlist=numpy.zeros(1500)
pulselist=numpy.arange(13,500,40)
stimlist[pulselist]=1 
pulselist2=numpy.arange(997,1500,40)
stimlist[pulselist2]=1    

#duration = .02*second

A2=TimedArray(stimlist*mV/mV,dt=.001*second)
I2=A2

defaultclock.dt=0.1*ms
tau_ampa=2*ms
tau_gaba=3*ms
eqs = '''
dv/dt = (0.04*v**2 + 5*v + 140 - u + mag1*I1(t)+mag2*I2(t) -g_ampa*(v))/ms: 1
du/dt = a*(b*v - u)/ms : 1
dg_ampa/dt = -g_ampa/tau_ampa : 1
a : 1
b : 1
c : 1
d : 1
mag1 : 1
mag2 : 1
x : meter
y : meter
std : 1
'''

Grs1 = NeuronGroup(1,eqs, clock=Clock(defaultclock.dt), threshold = 'v >= 30', method='euler',reset = '''
	v = c
	u = u + d 
''')
Grs2 = NeuronGroup(1,eqs, clock=Clock(defaultclock.dt), threshold = 'v >= 30', method='euler',reset = '''
	v = c
	u = u + d 
''')

taupre = taupost = 20*ms
wmax = 2*.8
Apre = 0.01
Apost = -Apre*taupre/taupost*1.05

Sr = Synapses(Grs1, Grs2, clock=Grs1.clock,method='euler',model='''
        	w : 1
        	dapre/dt = -apre/taupre : 1 (clock-driven) 
        	dapost/dt = -apost/taupost : 1 (clock-driven)
        	''',
		on_pre='''
		g_ampa += w
		apre += Apre
             	w = clip(w+apost, 0, wmax)
		''',
		on_post='''
		apost += Apost
		w = clip(w+apre, 0, wmax)
		''')
                            
                                                                                                   
Sr.connect(i=[0],j=[0])
Sr.w=.1
#Regular Spiking

Grs1.a = 0.02
Grs1.b = 0.2
Grs1.c = -65 
Grs1.d = (8 )
Grs1.v = -65
Grs1.u = Grs1.b*(Grs1.v)
Grs1.mag1=40
Grs1.mag2=0


Grs2.a = 0.02
#Gtc.b = 0.25
Grs2.b = 0.2
Grs2.c = -65 
#Gtc.d = 0.06
Grs2.d = 8.
Grs2.v = -65
Grs2.u = Grs2.b*(Grs2.v)
Grs2.mag1=0
Grs2.mag2=40


#M = StateMonitor(G,'v',record=True)
M = StateMonitor(Grs1,('v','g_ampa'),record=True)
M2 = StateMonitor(Grs2,('v','g_ampa'),record=True)
M3=StateMonitor(Sr,('apre','apost'),record=True)
run(duration)
subplot(511)
plot(M.t/ms, M.v[0])
subplot(512)
plot(M.t/ms, M2.g_ampa[0],'r')
subplot(513)
plot(M.t/ms, M2.v[0])
subplot(514)
plot(M.t/ms, M3.apre[0])
subplot(515)
plot(M.t/ms, M3.apost[0])
#vis_directed(Sre,Stc)
figure()
plot(M.t/ms, M.v[0])
plot(M.t/ms, M2.v[0],'r')




show()