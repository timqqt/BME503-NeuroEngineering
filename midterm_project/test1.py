import matplotlib.pyplot as plt
import time
a, b = range(100), range(100)
plt.ion()
plt.plot(a, b)
plt.show()
plt.pause(0.5)
plt.close('all')