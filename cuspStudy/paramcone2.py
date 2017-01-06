from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

# here i dont think X =Y would work because it would run into copy issues
X = np.arange(-5,5,0.25)
Y = np.arange(-5,5,0.25)

X,Y = np.meshgrid(X,Y)

Z = -(abs(X) + abs(Y))

## initial surface
X = X.flatten()
Y = Y.flatten()
Z = Z.flatten()

# cut off at a certain point
cut_idx = np.where(Z > -5)

#apply the "cut off"
Xc = X[cut_idx]
Yc = Y[cut_idx]
Zc = Z[cut_idx]

# you can use r to replace long strings

# plot the new surface (impossible with quad grid??)
surfc = ax.plot_trisurf(Xc,Yc,Zc,cmap=cm.jet,linewidth=0.2)

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(-10,0)
plt.show()
