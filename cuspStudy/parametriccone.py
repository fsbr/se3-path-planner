import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# pretty pathetic commit but I'm trying to write this cone for my cusp model

h = 1 
r = np.linspace(0,1)
u = np.linspace(0,h)
theta = np.linspace(0,2*np.pi)
x =((h-u)/(h))*r*np.cos(theta)
y =((h-u)/(h))*r*np.sin(theta)
z = u

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_wireframe(x,y,z, label='cone')
ax.legend()
plt.show()
