from spacepy import coordinates as coord
from spacepy.time import Ticktock
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#df = pd.read_csv('simpleorbit.csv')
df = pd.read_csv('01_Jan_2019.csv')
# df = pd.read_csv('Jan65.txt')
print(df.tail())
# i THINK this is what i need to get into the regular mjd timeframe
t = df['DefaultSC.A1ModJulian'] + 29999.5
#t = np.asarray(t)
#print(type(t))
x = df['DefaultSC.gse.X']
y = df['DefaultSC.gse.Y']
z = df['DefaultSC.gse.Z']
cvals = coord.Coords([[i,j,k] for i,j,k in zip(x,y,z)],'GSE','car')

# i'm pretty sure this serves zero purpose
cvals.x = x
cvals.y = y
cvals.z = z
cvals.ticks = Ticktock(t, 'MJD')
sm = cvals.convert('SM','car')
# gsm = cvals.convert('GEO', 'car')
# need to memorize how to do coordinates and time in spacepy

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(cvals.x,cvals.y,cvals.z, label='orbit')
# ax.plot(sm.x, sm.y, sm.z, label='sm orbit')
# ax.plot(gsm.x, gsm.y, gsm.z, label='gsm orbit')
ax.legend()
plt.show()
