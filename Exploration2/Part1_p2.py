from brian2 import *
# defaultclock.dt=.0005*ms
num_neurons = 1000
duration = 2000*ms
# Parameters for RS model
# a = 0.02
# b = 0.2
# c = -65*mV
# d = 8.0 * mV
# R = 1*ohm
# v0 = -65*mV
# u0 = 10.08089838*mV
# Parameters for IB model
# a = 0.02
# b = 0.2
# c = -55*mV
# d = 10.0 * mV
# R = 1*ohm
# v0 = -65*mV
# u0 = 0*mV
# Parameters for CH model
# a = 0.02
# b = 0.2
# c = -50*mV
# d = 3.0 * mV
# R = 1*ohm
# v0 = -65*mV
# u0 = 4*mV
# Parameters for FS model
a = 0.1
b = 0.2
c = -65*mV
d = 2.0 * mV
R = 1*ohm
v0 = -65*mV
u0 = 4*mV
#The model
eqs_fv = '''
fv = 0.04*v**2 / mV + 5*v + 140*mV : volt
 '''
eqs_u = '''
du/dt = a*(b*v - u) * metre ** 2 * kilogram * second ** -4 * amp ** -1 /mV: volt
'''
eqs = '''
dv/dt = (fv - u + R*I)* metre ** 2 * kilogram * second ** -4 * amp ** -1 /mV : volt
I : amp
'''
eqs += eqs_fv + eqs_u
# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs,
                    threshold='v >= 30*mV',
                    reset='v = c;u = u + d',
                    method='euler')
monitor2=StateMonitor(group, ('v', 'u'),  record=True)
group.v = -68.5*mV
group.u = b*(-68.5)*mV
group.I = 0*mA
run(10*ms)
group.v = v0
group.u = u0
group.I = '(70.0*mA * i) / num_neurons'

monitor = SpikeMonitor(group)

run(duration)
figure(1)
plot(monitor2.t/ms, monitor2.v[400]/mV) #plot the voltage for neuron 0 (index starts at 0)
xlim(0, 90)
ylim(-80, 40)
xlabel('t/ms')
ylabel('mV')
title('Fast Spiking (FS)')
# figure(2)
# plot(group.I/nA, (monitor.count / duration)/Hz)
# xlabel('I (nA)/I_threshold')
# ylabel('Firing rate (sp/s)')
# title('Curve of firing rate')
show()
