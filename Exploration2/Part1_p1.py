from brian2 import *
defaultclock.dt=.0005*ms
num_neurons = 100
duration = 20*ms
# Parameters
# area=20000*umetre**2 no more area for the neuron, the IAF model represents point(no area) neuron.
El = -65*mV
V_reset = -65*mV
V_th = -50*mV
tau_m = 10*ms
R_m = 10*Mohm
delta_e = 5.0*mV
VT = -55*mV
V_max = 30*mV



#The model
eqs_fv = '''
fv = delta_e * exp((v-VT)/delta_e) : volt
 '''


eqs = '''
d = El - v + fv + R_m*I : volt
dv/dt = (El - v + fv + R_m*I)/tau_m :  volt
I : amp
'''
eqs += (eqs_fv)

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs,clock=Clock(defaultclock.dt),
                    threshold='v >= V_max',
                    reset='v=V_reset',
                    method='euler')
monitor2=StateMonitor(group, ('v', 'd',),  record=True)
group.v = -65*mV

group.I = 0*nA
run(20*ms)
group.I = '(14.0*nA * i) / num_neurons'

monitor = SpikeMonitor(group)

run(duration)
figure(1)
plot(monitor2.t/ms, monitor2.v[40]/mV) #plot the voltage for neuron 0 (index starts at 0)
xlim(0, 70)

xlabel('t/ms')
ylabel('mV')
title('Output from neuron with stimulating current 3.5nA')
figure(2)
plot(group.I/nA, (monitor.count / duration)/Hz)
xlabel('I (nA)/I_threshold')
ylabel('Firing rate (sp/s)')
title('Curve of firing rate')
figure(3)
plot(monitor2.t/ms, monitor2.d[40])
xlim(0, 60)
show()