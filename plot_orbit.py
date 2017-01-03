# i need to plot the orbit of the datasets to ensure that they are right.

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
path = '/home/tckf/BostonUniversity/research/data-se3-path-planner/cherylData/'

df = pd.read_csv(path+'Jan80.txt')
df1 = pd.read_csv(path+'Jan55.txt')
df2 = pd.read_csv(path+'Jul80.txt')
print(df.tail())
x80 = df['DefaultSC.gse.X'][:1000]
y80 = df['DefaultSC.gse.Y'][:1000]
z80 = df['DefaultSC.gse.Z'][:1000]


x55 = df1['DefaultSC.gse.X'][:1000]
y55 = df1['DefaultSC.gse.Y'][:1000]
z55 = df1['DefaultSC.gse.Z'][:1000]
z55 = df1['DefaultSC.gse.Z'][:1000]

xjul55 = df2['DefaultSC.gse.X'][:1000]
yjul55 = df2['DefaultSC.gse.Y'][:1000]
zjul55 = df2['DefaultSC.gse.Z'][:1000]
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x80,y80,z80)
ax.plot(x55,y55,z55)
ax.plot(xjul55,yjul55,zjul55)
plt.show()



