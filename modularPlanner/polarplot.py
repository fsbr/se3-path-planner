"""
demo of a line plot on polar axis
"""

r = np.arange(0,3.0,0.01)
theta = 2*np.pi*r

ax = plt.subplot(111,projection='polar')
