import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# pretty pathetic commit but I'm trying to write this cone for my cusp model

h = 10 
#r = np.linspace(0,1)
r = 1
u = np.linspace(0,h,1000)
theta = np.linspace(0,2*np.pi,1000)
x =((h-u)/(h))*r*np.cos(theta)
y =((h-u)/(h))*r*np.sin(theta)
z = u

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(x,y,z, label='cone')
ax.legend()
plt.show()
