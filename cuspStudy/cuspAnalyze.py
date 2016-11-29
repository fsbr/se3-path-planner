# okay lets do this
import pandas as pd
import numpy as np
pathName = 'data/'
filesList = ['55deg.txt', '60deg.txt','65deg.txt', '70deg.txt', '75deg.txt','80deg.txt','85deg.txt']
filesList = [pathName+files for files in filesList]
anglesList = [55, 60, 65, 70, 75, 80, 85]

cma = []
npi = 0
for files in filesList:
    df = pd.read_csv(files)
    print(df.tail())
    Xgse =  df['DefaultSC.gse.X']
    Zgse =  df['DefaultSC.gse.Z']

    angle =  np.arctan2(df['DefaultSC.gse.Z'], df['DefaultSC.gse.X'])

    # make it into an array for iteration (probably a faster way)

    print(angle)
    print(len(angle))
    count = 0
    for x in angle:
        # These numbers are from the tsyganenko script that I wrote a while back
        if 0.2151<=x<=0.2849:
            count+=1

    print(count)
    cma.append([count])
    npi+=1

    print(cma)

from pylab import *
cdict = {'red': ((0.0, 0.0, 0.0),
                 (0.5, 1.0, 0.7),
                 (1.0, 1.0, 1.0)),
         'green': ((0.0, 0.0, 0.0),
                   (0.5, 1.0, 0.0),
                   (1.0, 1.0, 1.0)),
         'blue': ((0.0, 0.0, 0.0),
                  (0.5, 1.0, 0.0),
                  (1.0, 0.5, 1.0))}
my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
pcolor(cma,cmap=my_cmap)
colorbar()
plt.show()

