#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 12:06:14 2018

@author: chenriq
"""

from brian2 import *
defaultclock.dt= .001*ms
num_neurons = 2
duration = 2*second

# Parameters
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -60*mV
gl = 0.7*msiemens/cm**2

tau_ampa = 0.3*ms
g_synpk = 1.5
g_synmaxval = (g_synpk)
# eqs for neuron
eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (il +g_ampa*msiemens/cm**2*(-0*mV-v)+I/area )/Cm:  volt
dg_ampa/dt = -g_ampa/tau_ampa: 1
I : amp
'''
eqs += (eqs_il) 
# eqs for syn
eqs_syn = '''

'''
# Threshold and refractoriness are only used for spike counting
group1 = NeuronGroup(1, eqs, clock=Clock(defaultclock.dt),threshold='v > -45*mV',reset='v = -60*mV', method='euler')
group2 = NeuronGroup(1, eqs, clock=Clock(defaultclock.dt),threshold='v > -45*mV',reset='v = -60*mV', method='euler')
group1.v = El
group2.v = El

Sr = Synapses(group1, group2, clock=group1.clock, model='''
        g_synmax:1 ''', on_pre='''g_ampa+= g_synmax''')

Sr.connect('i == j')
Sr.g_synmax = g_synmaxval
Sr.delay = 1*ms #introduces a fixed delay between the firing of the pre cell  and the postsynaptic response

monitor1=StateMonitor(group1, ('v', 'g_ampa'), record=True)
monitor2=StateMonitor(group2, ('v', 'g_ampa'), record=True)

group1.I= 0*nA
group2.I = 0*nA
run(5.0*ms, report='text')
group1.I = 8*nA
group2.I = 0*nA
run(.5*ms, report='text')
group1.I = 0*nA
group2.I = 0*nA
run(10.0*ms)


figure(1)
subplot(4, 1, 1)
plot(monitor1.t/ms, monitor1.v[0]/mV)
subplot(4, 1, 2)
plot(monitor1.t/ms, monitor1.g_ampa[0])
subplot(4, 1, 3)
plot(monitor2.t/ms, monitor2.g_ampa[0], 'r')
subplot(4, 1, 4)
plot(monitor2.t/ms, monitor2.v[0]/mV, 'r')
show()