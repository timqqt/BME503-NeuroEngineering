from brian2 import *

num_neurons = 100
duration = 2*second

# Parameters
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -17.0*mV
EK = -72*mV
ENa = 55.0*mV
EA= -75.0*mV

gl = 0.3*msiemens/cm**2
gNa = 120.0*msiemens/cm**2
gK = 20*msiemens/cm**2
gA = 47.7*msiemens/cm**2

#The model
eqs_ina = '''
ina=gNa * m**3 * h * (ENa-v) :  amp/meter**2
dm/dt = alpham * (1-m) - betam * m : 1
dh/dt = alphah * (1-h) - betah * h : 1
alpham = 0.38/mV*(v+29.7*mV)/(1-exp(-0.1*(v+29.7*mV)/mV ) )/ms : Hz
betam = 15.2*exp(-0.0556*(v+54.7*mV)/mV)/ms : Hz
alphah = 0.266*exp(-0.05*(v+48*mV)/mV)/ms : Hz
betah = 3.8/(1+exp(-0.1*(v+18.*mV)/mV))/ms : Hz
'''




eqs_iA = '''
iA=gA * a**3 * b * (EA-v) :  amp/meter**2
a_inf = (((0.0761*exp(0.0314*(v+94.22*mV)/mV))/(1+exp(0.0346*(v+1.17*mV)/mV)))**(1/3)) : 1
b_inf = ((1/(1+exp(0.0688*(v+53.3*mV)/mV)))**4) : 1
da/dt = (a_inf - a)/tau_a : 1
db/dt = (b_inf - b)/tau_b : 1
tau_a = (0.3632 + (1.158/(1+exp(0.0497*(v+55.96*mV)/mV))))*ms : second
tau_b = (1.24 + (2.678/(1+exp(0.0624*(v+50*mV)/mV))))*ms : second
'''

eqs_ik = '''
ik=gK * n**4 * (EK-v):amp/meter**2
dn/dt = alphan * (1-n) - betan * n : 1
alphan = (0.02*(v+45.7*mV)/mV)/(1-exp(-0.1*(v+45.7*mV)/mV))/ms : Hz
betan = 0.25*exp(-0.0125*(v+55.7*mV)/mV)/ms : Hz
'''

eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (ina+ik+il+iA+I/area)/Cm:  volt
I : amp
'''
eqs += (eqs_ina+eqs_ik+eqs_il+eqs_iA)
# re-run spikes
# Threshold and refractoriness are only used for spike counting

group = NeuronGroup(num_neurons, eqs,
                    threshold='v > -40*mV',
                    refractory='v > -40*mV',
                    method='exponential_euler')
# group.v = -90.0*mV
# # group.m=0.0529
# # group.n=0.3177
# # group.h=0.596
# group.m=0
# group.n=0
# group.h=1
group.v = -89.79961487*mV
group.m=0.00052483
group.n=0.02756506
group.h=0.99865692
group.a = 0.4371503
group.b =0.73184542
group.I = -13.0*nA
monitor2=StateMonitor(group,'v',record=True)
run(50.0*ms)
group.I = '(7.0*nA * i) / num_neurons'

monitor = SpikeMonitor(group)

run(duration)
fig = figure(figsize=(7, 7))

ax4 = fig.add_subplot(224)
plot(monitor2.t/ms, monitor2.v[28]/mV) #plot the voltage for neuron 0 (index starts at 0)
xlim(0, 200)
xlabel('t/ms')
ylabel('mV')

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs,
                    threshold='v > -40*mV',
                    refractory='v > -40*mV',
                    method='exponential_euler')
group.v = -66.76811498*mV
group.m=0.01287421
group.n=0.67802686
group.h=0.26582129
group.a=0.7364238
group.b=0.03608132
# group.v = -70.0*mV
# group.m=0.0
# group.n=0.7
# group.h=0.5


monitor2=StateMonitor(group, 'v', record=True)

group.I = '(7.0*nA * i) / num_neurons'

monitor = SpikeMonitor(group)

run(duration)

ax1 = fig.add_subplot(221)
plot(group.I/nA/1.615, (monitor.count / duration)/Hz)
xlim(0.9, 1.5)
xticks(arange(0.9, 1.6, 0.1))
ylim(0, 60)
xlabel('I (nA)/I_threshold')
ylabel('Firing rate (sp/s)')
ax2 = fig.add_subplot(222)
plot(monitor2.t/ms, monitor2.v[29]/mV) #plot the voltage for neuron 0 (index starts at 0)
xlim(0, 100)
xlabel('t/ms')
ylabel('mV')


# turned off
gA=  0 *msiemens/cm**2
El = -70*mV
num_neurons = 1000
# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs,
                    threshold='v > -40*mV',
                    refractory='v > -37.0*mV',
                    method='exponential_euler')
group.v = -68.0*mV
group.m=0.0529
group.n=0.3177
group.h=0.596

monitor2=StateMonitor(group, 'v', record=True)

group.I = '(7.0*nA * i) / num_neurons'

monitor = SpikeMonitor(group)

run(duration)
ax3 = fig.add_subplot(223)
plot(group.I/nA/1.58, (monitor.count / duration)/Hz)
xlim(0.9, 1.3)
ylim(0, 200)
xlabel('I (nA)/I_threshold')
ylabel('Firing rate (sp/s)')
print(where((monitor.count / duration)/Hz > 100))
print(7*min(where((monitor.count / duration)/Hz > 100))/num_neurons)
show()