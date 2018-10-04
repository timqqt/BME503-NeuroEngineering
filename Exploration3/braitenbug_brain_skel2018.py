from brian2 import *
import matplotlib.pyplot as plt

map_size = 100
global foodx, foody, food_count, bug_plot, food_plot, sr_plot, sl_plot, outbugx, outbugy, outbugang, outfoodx, outfoody, outsrx, outsry, outslx, outsly

food_count = 0
foodx = 50
foody = 50
duration = 50
outbugx = np.zeros(int(duration / 2))
outbugy = np.zeros(int(duration / 2))
outbugang = np.zeros(int(duration / 2))
outfoodx = np.zeros(int(duration / 2))
outfoody = np.zeros(int(duration / 2))
outsrx = np.zeros(int(duration / 2))
outsry = np.zeros(int(duration / 2))
outslx = np.zeros(int(duration / 2))
outsly = np.zeros(int(duration / 2))

# Sensor neurons
a = 0.02
b = 0.2
c = -65
d = 0.5


I0 = 1250
tau_ampa = 1.0 * ms
g_synpk = 0.4
g_synmaxval = (g_synpk / (tau_ampa / ms * exp(-1)))

sensor_eqs = '''

x : 1
y : 1
x_disp : 1
y_disp : 1
foodxx : 1
foodyy : 1
mag :1
I = I0 / sqrt(((x-foodxx)**2+(y-foodyy)**2)): 1

dv/dt = (fv - u + mag*I + z*(0-v))/ms : 1
dz/dt = -z/tau_ampa : 1
fv = 0.04*v**2 + 5*v + 140 : 1
du/dt = a*(b*v - u)/ms : 1
'''

sensor_reset = '''
v = c
u = u + d
'''

sr = NeuronGroup(1, sensor_eqs, clock=Clock(0.2 * ms), threshold="v>=30", reset=sensor_reset, method='euler')
sr.v = c
sr.u = c * b
sr.x_disp = 5
sr.y_disp = 5
sr.x = sr.x_disp
sr.y = sr.y_disp
sr.foodxx = foodx
sr.foodyy = foody
sr.mag = 1

sl = NeuronGroup(1, sensor_eqs, clock=Clock(0.2 * ms), threshold="v>=30", reset=sensor_reset, method='euler')
sl.v = c
sl.u = c * b
sl.x_disp = -5
sl.y_disp = 5
sl.x = sl.x_disp
sl.y = sl.y_disp
sl.foodxx = foodx
sl.foodyy = foody
sl.mag = 1

sbr = NeuronGroup(1, sensor_eqs, clock=Clock(0.2 * ms), threshold="v>=30", reset=sensor_reset, method='euler')
sbr.v = c
sbr.u = c * b
sbr.foodxx = foodx
sbr.foodyy = foody
sbr.mag = 0

sbl = NeuronGroup(1, sensor_eqs, clock=Clock(0.2 * ms), threshold="v>=30", reset=sensor_reset, method='euler')
sbl.v = c
sbl.u = c * b
sbl.foodxx = foodx
sbl.foodyy = foody
sbl.mag = 0

# The virtual bug

taum = 4 * ms
base_speed = 9.5
turn_rate = 5 * Hz

bug_eqs = '''
#equations for movement here
dx/dt = motor * cos(angle)/ms : 1
dy/dt = motor * sin(angle) /ms : 1
motor = (motorl + motorr)/2 : 1
dangle/dt = ((motorr - motorl)/(5*sqrt(2)))/ms : 1
dmotorl/dt = - (motorl/taum) : 1
dmotorr/dt = - (motorr/taum) : 1

'''

bug = NeuronGroup(1, bug_eqs, clock=Clock(0.2 * ms), method='euler')
bug.motorl = 0
bug.motorr = 0
bug.angle = pi / 2
bug.x = 0
bug.y = 0

# Synapses (sensors communicate with bug motor)
w = 10
syn_rr = Synapses(sr, sbl, clock=Clock(0.2 * ms), model='''
                g_synmax:1
                ''',
                  on_pre='''
		z+= g_synmax
		''')

syn_rr.connect(i=[0], j=[0])
syn_rr.g_synmax = g_synmaxval

syn_ll = Synapses(sl, sbr, clock=Clock(0.2 * ms), model='''
                g_synmax:1
                ''',
                  on_pre='''
		z+= g_synmax
		''')

syn_ll.connect(i=[0], j=[0])
syn_ll.g_synmax = g_synmaxval

syn_r = Synapses(sbr, bug, clock=Clock(0.2 * ms), on_pre='motorr += w')
syn_r.connect(i=[0], j=[0])
syn_l = Synapses(sbl, bug, clock=Clock(0.2 * ms), on_pre='motorl += w')
syn_l.connect(i=[0], j=[0])

# Step for show figure
step = 0
f = figure(1)
bug_plot = plot(bug.x, bug.y, 'ko')
food_plot = plot(foodx, foody, 'b*')
sr_plot = plot([0], [0], 'w')  # Just leaving it blank for now
sl_plot = plot([0], [0], 'w')
title("Time: "+str(2*step)+"ms")


# Additional update rules (not covered/possible in above eqns)

@network_operation()
def update_positions():

    global foodx, foody, food_count
    sr.x = bug.x + sr.x_disp * sin(bug.angle) + sr.y_disp * cos(bug.angle)
    sr.y = bug.y + - sr.x_disp * cos(bug.angle) + sr.y_disp * sin(bug.angle)

    sl.x = bug.x + sl.x_disp * sin(bug.angle) + sl.y_disp * cos(bug.angle)
    sl.y = bug.y - sl.x_disp * cos(bug.angle) + sl.y_disp * sin(bug.angle)

    if ((bug.x - foodx) ** 2 + (bug.y - foody) ** 2) < 16:
        food_count += 1
        foodx = randint(-map_size + 10, map_size - 10)
        foody = randint(-map_size + 10, map_size - 10)

    if (bug.x < -map_size):
        bug.x = -map_size
        bug.angle = pi - bug.angle
    if (bug.x > map_size):
        bug.x = map_size
        bug.angle = pi - bug.angle
    if (bug.y < -map_size):
        bug.y = -map_size
        bug.angle = -bug.angle
    if (bug.y > map_size):
        bug.y = map_size
        bug.angle = -bug.angle

    sr.foodxx = foodx
    sr.foodyy = foody
    sl.foodxx = foodx
    sl.foodyy = foody


@network_operation(dt=2 * ms)
def update_plot(t):
    global foodx, foody, bug_plot, food_plot, sr_plot, sl_plot, outbugx, outbugy, outbugang, outfoodx, outfoody, outsrx, outsry, outslx, outsly, step
    step += 1
    if step % 10 == 0:
        print('Close all figures')
        plt.close('all')
    indx = int(.5 * t / ms + 1)
    bug_plot[0].remove()
    food_plot[0].remove()
    sr_plot[0].remove()
    sl_plot[0].remove()
    bug_x_coords = [bug.x, bug.x - 4 * cos(bug.angle), bug.x - 8 * cos(bug.angle)]  # ant-like body
    bug_y_coords = [bug.y, bug.y - 4 * sin(bug.angle), bug.y - 8 * sin(bug.angle)]
    outbugx[indx - 1] = bug.x[0]
    outbugy[indx - 1] = bug.y[0]
    outbugang[indx - 1] = bug.angle[0]
    outfoodx[indx - 1] = foodx
    outfoody[indx - 1] = foody
    outsrx[indx - 1] = sr.x[0]
    outsry[indx - 1] = sr.y[0]
    outslx[indx - 1] = sl.x[0]
    outsly[indx - 1] = sl.y[0]
    bug_plot = plot(bug_x_coords, bug_y_coords, 'ko')  # Plot the bug's current position
    sr_plot = plot([bug.x, sr.x], [bug.y, sr.y], 'b')
    sl_plot = plot([bug.x, sl.x], [bug.y, sl.y], 'r')
    food_plot = plot(foodx, foody, 'b*')
    axis([-100, 100, -100, 100])
    title("Time: "+str(2*step)+"ms")
    draw()

    # print "."
    pause(0.05)


# ML = StateMonitor(sl, ('v', 'I'), record=True)
# MR = StateMonitor(sr, ('v', 'I'), record=True)
# MB = StateMonitor(bug, ('motorl', 'motorr', 'speed', 'angle', 'x', 'y'), record = True)
run(duration * ms, report='text')
np.save('outbugx', outbugx)
np.save('outbugy', outbugy)
np.save('outbugang', outbugang)
np.save('outfoodx', outfoodx)
np.save('outfoody', outfoody)
np.save('outsrx', outsrx)
np.save('outsry', outsry)
np.save('outslx', outslx)
np.save('outsly', outsly)









