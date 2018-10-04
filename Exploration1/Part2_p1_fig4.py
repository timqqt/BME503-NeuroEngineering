from brian2 import *

num_neurons = 1
duration = 30*ms

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
group.v = -89.79961487*mV
group.m=0.00052483
group.n=0.02756506
group.h=0.99865692
group.a = 0.4371503
group.b =0.73184542
# group.m=0
# group.n=0
# group.h=1
monitor2=StateMonitor(group, 'v', record=True)
monitor3=StateMonitor(group, 'm', record=True)
monitor4=StateMonitor(group, 'n', record=True)
monitor5=StateMonitor(group, 'h', record=True)
monitor6=StateMonitor(group, 'a', record=True)
monitor7=StateMonitor(group, 'b', record=True)

monitor2=StateMonitor(group,'v',record=True)
group.I = -13.0*nA
run(duration)
fig = figure(figsize=(7, 7))
plot(monitor2.t/ms, monitor2.v[29]/mV) #plot the voltage for neuron 0 (index starts at 0)
# xlim(0, 200)
xlabel('t/ms')
ylabel('mV')
print( monitor2.v[29]/mV)
print(monitor3.m[29])
print(monitor4.n[29])
print(monitor5.h[29])
print(monitor6.a[29])
print(monitor7.b[29])

show()