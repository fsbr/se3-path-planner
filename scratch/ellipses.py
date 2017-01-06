import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# spacepy
from spacepy.coordinates import Coords

axisUpperBound = 2
axisLowerBound = -2
t = np.linspace(0,2*np.pi, 1000)
a = 1 
b = 0.5
x = a*np.cos(t)
y = b*np.sin(t)
# put to spacepy
# okay i really need to run a gmat simulation in order to do this
x1 = np.cos(t)
x2 = np.sin(t)

# put these fake elliptical coords to spacepy coords object
cvals = coord.Coords(x,y,'GSE','car')

# okay so i think this works, but it kinda makes things which are actually ellipses
# look like a fucking circle
# 2a = major axis
# 2b = minor axis
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x,y)
ax.plot(x1,x2)
ax.set_xlim(axisLowerBound,axisUpperBound)
ax.set_ylim(axisLowerBound,axisUpperBound)
plt.show()
