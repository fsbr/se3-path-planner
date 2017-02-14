# i'm going to try to apply the interpolation to the data using the simple
# scipy model that i found.

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pathname = '../../batch2019/'
sys.path.append(pathname)
df = pd.read_csv(pathname + 'Jun80_results.csv')
Re = 6371
GMAT_MJD_OFFSET = 29999.5

t = df['DefaultSC.A1ModJulian'] + GMAT_MJD_OFFSET
x = df['DefaultSC.gse.X']
y = df['DefaultSC.gse.Y']
z = df['DefaultSC.gse.Z']
# print(t)
tStart= t[0]
tEnd = t[len(t)-1]
tInterval = (t[1]-t[0])/100 # i want to do 100 but it takes a while
# for some reason, arange works and linspace doesnt.
tnew = np.arange(tStart, tEnd, tInterval)
xnew = np.interp(tnew,t,x)
ynew = np.interp(tnew,t,y)
znew = np.interp(tnew,t,z)
print(z)
print(znew)
plt.plot(t,x,'o')
plt.plot(tnew,xnew,'x')
plt.show()

plt.plot(t,z,'o')
plt.plot(tnew,znew,'x')
plt.show()

