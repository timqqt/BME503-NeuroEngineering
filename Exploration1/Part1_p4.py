from brian2 import *

num_neurons = 1000
num_E_rest = -60
# Parameters
area=20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -49.387*mV
EK = -72.0*mV
ENa = 55.0*mV
E_rest = -60*mV
duration = 2*second
gl = 0.3*(msiemens)/(cm**2)
gNa = 120.0*(msiemens)/(cm**2)
gK = 36.0*(msiemens)/(cm**2)


#The model
eqs_ina = '''
ina=gNa * m**3 * h * (ENa-(v)) :  amp/meter**2

dm/dt = alpham * (1-m) - betam * m : 1
dh/dt = alphah * (1-h) - betah * h : 1

alpham = (0.1/mV) * (-(v+60*mV)+25*mV) / (exp((-(v+60*mV)+25*mV) / (10*mV)) - 1) /ms : Hz
betam = 4*exp(-(v+60*mV)/(18*mV))/ms : Hz
alphah = 0.07*exp(-(v+60*mV)/(20*mV))/ms : Hz
betah = 1/(exp((-(v+60*mV)+30*mV) / (10*mV))+1)/ms : Hz
'''

eqs_ik = '''
ik=gK * n**4 * (EK-v):amp/meter**2

dn/dt = alphan * (1-n) - betan * n : 1

alphan = (0.01/mV) * (-(v+60*mV)+10*mV) / (exp((-(v+60*mV)+10*mV) / (10*mV)) - 1)/ms : Hz
betan = 0.125*exp(-(v+60*mV)/(80*mV))/ms : Hz
'''

eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (ina+ik+il +I/area)/Cm :  volt
I : amp
'''
eqs += (eqs_ina+eqs_ik+eqs_il)

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs,
                    threshold='v > -40*mV',
                    refractory='v > -35*mV',
                    method='exponential_euler')
group.v = -60*mV
group.m=0.0529
group.n=0.3177
group.h=0.596

monitor2=StateMonitor(group,'v',record=True)

group.I = '(7.0*nA * i) / num_neurons'
monitor = SpikeMonitor(group)
run(duration)
print(monitor.count)
figure(1)
plot(group.I/nA/1.3, (monitor.count / duration)/Hz)
xlim(0.9, 1.3)
xlabel('I (nA)/I_threshold')
ylabel('Firing rate (sp/s)')

show()