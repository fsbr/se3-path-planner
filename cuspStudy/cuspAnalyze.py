#2 okay lets do this
import sys
sys.path.append('../.')
import pandas as pd
import numpy as np
import itertools as it
import path_planner as plan
pathName = '../../data-se3-path-planner/cherylData/'
pathName1 = '../../data-se3-path-planner/yearData/batch2019/'
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
inclinations = ['55', '60', '65', '70', '75', '80', '85', '90']
inclinations = inclinations[::-1] # reverses the inclinations 

filesList =[[pathName+month+inclination+'.txt' for month in months ] for inclination in inclinations] 
# print( filesList)
# filesList = ['55deg.txt', '60deg.txt','65deg.txt', '70deg.txt', '75deg.txt','80deg.txt','85deg.txt']
# filesList = [pathName+files for files in filesList]
# filesList = ['80deg.txt']
# anglesList = [55, 60, 65, 70, 75, 80, 85]

cma = []
    
def createCma(files):
    # print("FILES", files)
    df = pd.read_csv(files)
    # print(df.tail())
    Xgse =  df['DefaultSC.gse.X']
    Ygse =  df['DefaultSC.gse.Y']
    Zgse =  df['DefaultSC.gse.Z']

    # i am DEFINITELY going to end up with a dimension problem here
    t = df['DefaultSC.A1ModJulian']
    # print(t.tail())
    t = t.tolist()
    t = [t_index + 29999.5 for t_index in t]
    # print("hopefully something close to the real time", t)
   #  print("type of t", type(t.tolist()))

    # refer to tsyganenko for these coordinate systems
    # the output here is in radians
    # angle = np.arctan2(Xgse,Zgse)
    # theta = np.arctan2(Ygse,Xgse)
    angle = np.arctan2(Zgse,Xgse)
    theta = np.arctan2(Xgse,Ygse)
    print("type angle,", type(angle))
    # but sometimes i print it in degrees
    # print("angle is" , angle * 180 / np.pi)
    # print("theta is", theta)

    # make it into an array for iteration (probably a faster way)

    # print(angle)
    # print(len(angle))
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
    # Okay I think I did it
    lowBound,highBound,lowLateralBound,highLateralBound = plan.GridGraph().getGoalRegion(t)
    # print("type of llb", lowLateralBound)
    # print("type of lb", lowBound)
    # print("type of hb", highBound)
    # print("type of llb", lowLateralBound)
    # print("type of hlb", highLateralBound)
    # lowBound = np.asarray(lowBound).tolist()
    # highBound = np.asarray(highBound).tolist()
    # lowLateralBound = np.asarray(lowLateralBound).tolist()
    # highLateralBound = np.asarray(highLateralBound).tolist()
    # print("lowbound hadhasdf", len(lowBound))
    # print("lowbound", lowBound)
    # print("highBound", highBound)
    # print("lowLateralBound", lowLateralBound)
    # print("highLateralbound", highLateralBound)
    # lowBound = 0.2151/2
    # highBound = 0.2849/2
    # lateralBound = 5.0/2


    # implement the tsyganenko function and dipole tilt for dynamic changing
    # of the cusp location
    # for x,y,lb,ub,llb,hlb in zip(angle, theta, lowBound, highBound, lowLateralBound, highLateralBound):
    for x,y,lb,hb,llb,hlb in zip(angle,theta,lowBound,highBound,lowLateralBound,highLateralBound):
         
        # the biggest thing is a modification of these thresholds
        # if lowBound<=x<=highBound and lowLateralBound<=y<=highLateralBound:
        if lb<=x<=hb and llb<=y<=hlb:
            # if lowLateralBound<=y<=highLateralBound:
            region.append(1)
        else:
            region.append(0) 

    for x,x1 in zip(region, region[1:]):
        if x==0 and x1 == 1:
            count+=1 
        else:
            pass
    # print("x", angle)
    # print("x1", angle[1:])
    
    # print("count",count)

    # the main problem is with the dimensions of the cma variable
    # so how do i get cma to have the same dimensions as filesList?
    cma.append([count])

    # print("cma", cma)
    # print("region",region)
    # print("region", region[:100])
    return count

cma2 =[]

# the fact that you can call a function in a list comprehension is the number one reason
# why i'm going to stick with python
cma2  =[[createCma(pathName1+month+inclination+'.txt') for month in months ] for inclination in inclinations] 
# cma2 = [[createCma(pathName1+'test4.txt')]]
print("cma2", cma2)

if __name__ == "__main__":
    a = 3
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
    pcolor(cma2,cmap=my_cmap)
    colorbar()
    plt.title('Cusp Crossings')
    plt.xlabel('Start Month')
    plt.ylabel('55+5y deg inclination')
    plt.show()

