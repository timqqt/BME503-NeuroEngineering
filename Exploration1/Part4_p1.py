from brian2 import *

num_neurons = 100
duration = 2000*ms
# Parameters
area=20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -60*mV
EK = -72.0*mV
ENa = 55.0*mV
E_rest = -60*mV

gl = 0.3*(msiemens)/(cm**2)
gNa = 120.0*(msiemens)/(cm**2)
gK = 36.0*(msiemens)/(cm**2)


#The model
eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (il +I/area)/Cm :  volt
I : amp
'''
eqs += (eqs_il)

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs,
                    threshold='v > -40*mV',
                    reset='v=-60*mV',
                    method='euler')
group.v = -60*mV
monitor2=StateMonitor(group,'v',record=True)
group.I = '(7.0*nA * i) / num_neurons'

monitor = SpikeMonitor(group)

run(duration)
figure(1)
plot(monitor2.t/ms, monitor2.v[99]/mV) #plot the voltage for neuron 0 (index starts at 0)
xlim(0, 3)
xlabel('t/ms')
ylabel('mV')
title('Output from neuron 75 ')
figure(2)
plot(group.I/nA, (monitor.count / duration)/Hz)
xlabel('I (nA)/I_threshold')
ylabel('Firing rate (sp/s)')
show()