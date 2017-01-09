# attempting to implement the parametric equations of a cone
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# from http://mathworld.wolfram.com/Cone.html
h = 1
r = 1 # r is a constant
u = np.linspace(0,h)
tht = np.linspace(0,2*np.pi)
x = ((h-u)/(h))*r*np.cos(tht)
y = ((h-u)/(h))*r*np.sin(tht)
z = u
x,y = np.meshgrid(x,y)

fig = plt.figure()
ax = plt.subplot(111,projection='3d') 
ax.plot_surface(x,y,z)
ax.legend()
plt.show()
