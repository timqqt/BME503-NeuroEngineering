from brian2 import *

num_neurons = 100
num_E_rest = -60
# Parameters
area=20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -50.613*mV
EK = -72.0*mV
ENa = 55.0*mV
E_rest = num_E_rest*mV

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
                    threshold='v > -100*mV',
                    refractory='v > -100*mV',
                    method='exponential_euler')
group.v = -60*mV
group.m=0.0529
group.n=0.3177
group.h=0.596

monitor2=StateMonitor(group,'v',record=True)
group.I = 0*nA
run(5.0*ms,report='text')
for i in range(num_neurons):
    group.I[i] = (7.0*nA * i) / num_neurons

# group.I[0] = 1.50*nA
# group.I[1] = 2.50*nA
run(2000*ms, report='text')
group.I = 0*nA
run(14.0*ms)

signal = 0
figure(1)
for ii in range(num_neurons):
    plot(monitor2.t / ms, monitor2.v[ii] / mV)  # plot the voltage for neuron 0 (index starts at 0)
    if max(monitor2.v[ii] / mV) > 0 and signal == 0:
        print("The "+ str(ii)+ " neuron is fired, and the amplitude of current is " + str(1.50 + ii * 0.1) + "nA")
        signal = 1
# plot(monitor2.t/ms, monitor2.v[0]/mV) #plot the voltage for neuron 0 (index starts at 0)
# plot(monitor2.t/ms, monitor2.v[1]/mV) #plot the voltage for neuron 0 (index starts at 0)
ylim(-90, 50) #set axes limits
# xlim(0, 20)
xlabel('Time (ms)')
ylabel('Voltage (mV)')
legend()
title('Hodgkin-Huxley Action Potential, Rest Potential ='+ str(num_E_rest) + ' mV')

#You can dump your results to a file to visualize separately
savetxt('Vmdata.dat',(monitor2.t/ms, monitor2.v[0]/mV))
#out=np.loadtxt('Vmdata.dat')
#plot(out[0],out[1])
show()