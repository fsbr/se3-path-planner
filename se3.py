# I'm trying to do SE(3) Lie group in python and plot in matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# the se(3) group is a composition of matrices in the following arrangement
# [r t; 0 1]
# tht = np.pi/4
tht = np.pi/2
# let's do a simple case of 3x3 matrices
# note that eventually the "r" matrix is going to have a composition of all 3 euler angles
# and that the angle order will matter
r = np.array([[np.cos(tht), np.sin(tht), 0],[-np.sin(tht), np.cos(tht), 0], [0, 0, 1]]) # 3x3
t = np.array([[2],[0],[0]])# 3x1
zeroMatrix = np.array([0,0,0]) #1x3
oneMatrix = np.array([1]) # 1x1

# np.hstack and np.vstack are how you make a "partitioned" matrix
# don't use the "partition" documetnation that's for something else
se3top = np.hstack((r,t))
se3bottom = np.hstack((zeroMatrix, oneMatrix))
se3 = np.vstack((se3top,se3bottom))
# se3 = np.array([[r, t],[zeroMatrix, oneMatrix]])
print "se3",se3
print "se3 dimensions", se3.shape
# weird cos it kinda prints like the composition of the matrices

# i think the final element of the coordinate vector is just a zero to fill it out
# if i put 1 there, then there are additional ones in the outputs. lame
# the multiplied vector has (x0,x1,x2,1) as its space
x = np.array([[1],[0],[0],[1]])
y = np.array([[0],[1],[0],[1]])
z = np.array([[0],[0],[1], [1]])
se3x = np.dot(se3,x)
se3y = np.dot(se3,y)
print "x",x
print "x0", se3x[0]
print "x1", se3x[1]
print "x2", se3x[2]
print "se3x",se3x
print "se3y", se3y
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[0],x[1],x[2])
ax.scatter(se3x[0],se3x[1],se3x[2])
ax.set_xlabel('x')
ax.set_xlabel('y')
ax.set_xlabel('z')
plt.show()

# so i think this works.
#
