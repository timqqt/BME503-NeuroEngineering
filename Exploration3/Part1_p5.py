from brian2 import *
defaultclock.dt=.01*ms
num_neurons = 2
duration = 2*second

# Parameters
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -60*mV
gl = 0.7*msiemens/cm**2

tau_ampa=0.3*ms
g_synpk= 800 * siemens
g_synmaxval=(g_synpk)
E_syn_in = -80*mV
E_syn_ex = 0*mV
tau_m = 5*ms
# Parameters for LTS model
a = 0.02
b = 0.25
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
dv/dt = ((fv - u + R*I)* metre ** 2 * kilogram * second ** -4 * amp ** -1 /mV) + (g*(E_syn-v)*metre ** 2 * kilogram * second ** -4 * amp ** -1/amp) : volt
I : amp
E_syn : volt 
'''
eqs_syn = '''
# The conductance of the alpha model
dz/dt = (-z/tau_m) : siemens
dg/dt = -g/tau_m + z/ms : siemens
'''

eqs += eqs_fv + eqs_u + eqs_syn
# Threshold and refractoriness are only used for spike counting
neuron1 = NeuronGroup(1, eqs,
                    threshold='v >= 30*mV',
                    reset='v = c;u = u + d',
                    method='euler'
                    )
neuron2 = NeuronGroup(1, eqs,
                    threshold='v >= 30*mV',
                    reset='v = c;u = u + d',
                    method='euler'
                      )
neuron3 = NeuronGroup(1, eqs,
                    threshold='v >= 30*mV',
                    reset='v = c;u = u + d',
                    method='euler'
                      )
neuron4 = NeuronGroup(1, eqs,
                    threshold='v >= 30*mV',
                    reset='v = c;u = u + d',
                    method='euler'
                      )
syn1 = Synapses(neuron1, neuron2, clock=neuron1.clock, on_pre='''g += g_synpk''')
syn2 = Synapses(neuron2, neuron3, clock=neuron2.clock, on_pre='''g += g_synpk''')
syn3 = Synapses(neuron3, neuron4, clock=neuron2.clock, on_pre='''g += g_synpk''')

syn1.connect('i == j')
syn2.connect('i == j')
syn3.connect('i == j')
# syn1.delay=10*ms
# syn2.delay=20*ms
syn3.delay = 0*ms

monitor1=StateMonitor(neuron1, ('v', 'g'), record=True)
monitor2=StateMonitor(neuron2, ('v', 'g'), record=True)
monitor3=StateMonitor(neuron3, ('v', 'g'), record=True)
monitor4=StateMonitor(neuron4, ('v', 'g'), record=True)

neuron1.v= -65*mV
neuron1.u= b*(-65*mV)
neuron2.v= -65*mV
neuron2.u= b*(-65*mV)
neuron3.v= -65*mV
neuron3.u= b*(-65*mV)
neuron4.v= -65*mV
neuron4.u= b*(-65*mV)


neuron1.g= 0*nsiemens
neuron2.g = 0*nsiemens
neuron3.g = 0*nsiemens
neuron4.g = 0*nsiemens

run(200.0*ms, report='text')
# Define the type of neuron
neuron1.E_syn = E_syn_ex
neuron2.E_syn = E_syn_ex
neuron3.E_syn = 1.5 * E_syn_in
neuron4.E_syn = E_syn_ex

neuron1.I = 0*mA
neuron2.I = 0*mA
neuron3.I = 40*mA
neuron4.I = 0*mA
run(20.0*ms, report='text')
neuron2.u= b*(-65*mV)
neuron1.I = 0*mA
neuron2.I = 0*nA
neuron3.I = 0*nA
neuron4.I = 0*mA
run(200.0*ms, report='text')


figure(1, figsize=(10, 10))
subplot(8, 1, 1)
plot(monitor1.t/ms, monitor1.v[0]/mV, 'g')
xlim(150, 300)
subplot(8, 1, 2)
plot(monitor1.t/ms, monitor1.g[0]/1000, 'g')
xlim(150, 300)
subplot(8, 1, 3)
plot(monitor2.t/ms, monitor2.v[0]/mV, 'r')
xlim(150, 300)
subplot(8, 1, 4)
plot(monitor2.t/ms, monitor2.g[0]/1000, 'r')
xlim(150, 300)
subplot(8, 1, 5)
plot(monitor3.t/ms, monitor3.v[0]/mV, 'b')
xlim(150, 300)
subplot(8, 1, 6)
plot(monitor3.t/ms, monitor3.g[0]/1000, 'b')
xlim(150, 300)
subplot(8, 1, 7)
plot(monitor4.t/ms, monitor4.v[0]/mV, 'chocolate')
xlim(150, 300)
subplot(8, 1, 8)
plot(monitor4.t/ms, monitor4.g[0]/1000, 'chocolate')
xlim(150, 300)
show()