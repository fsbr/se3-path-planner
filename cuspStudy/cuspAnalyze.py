# okay lets do this
import pandas as pd
import numpy as np
import itertools as it
pathName = '../../data-se3-path-planner/data/'
filesList = ['55deg.txt', '60deg.txt','65deg.txt', '70deg.txt', '75deg.txt','80deg.txt','85deg.txt']
filesList = [pathName+files for files in filesList]
# filesList = ['80deg.txt']
anglesList = [55, 60, 65, 70, 75, 80, 85]

cma = []
for files in filesList:
    df = pd.read_csv(files)
    print(df.tail())
    Xgse =  df['DefaultSC.gse.X']
    Ygse =  df['DefaultSC.gse.Y']
    Zgse =  df['DefaultSC.gse.Z']

    # angle =  np.arctan2(Zgse, Xgse)
    angle = np.arctan2(Xgse,Zgse)
    theta = np.arctan2(Ygse,Xgse)
    angleTotal = [angle, theta]
    # thresh = np.arctan2

    # make it into an array for iteration (probably a faster way)

    print(angle)
    print(len(angle))
    count = 0
    region = []
    # for x,x1 in zip(angle, angle[1:]):
        # eventually this has to be modified so that the unh professors script
        # will alter the dipole angle
        # These numbers are from the tsyganenko script that I wrote a while back
        # if x<0.2151 or x> 0.2849:
        #     if 0.2151<=x1<=0.2849:
                # count+=1
    # angle = angle[:20]
    # lets get this boundary crossing thing right
    for x,y in zip(angle, theta):
        if 0.2151<=x<=0.2849:
            # we can add in the other dimension right here
            if abs(y)> 5*np.pi/180:
                region.append(1)
        else:
            region.append(0) 

    for x,x1 in zip(region, region[1:]):
        if x==0 and x1 == 1:
            count+=1 
        else:
            print("not in the cusp yo.")
    print("x", angle)
    print("x1", angle[1:])
    
    print("count",count)
    cma.append([count])

    print("cma", cma)
    print("region",region)
    print("region", region[:100])


if __name__ == "__main__":

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

