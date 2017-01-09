# What I"m trying to do here is program the tysganenko model so that the plots actually
# look something like they do in the tsyganenko paper.
# I really want to have this done by monday but we will see
# tckf jan 2017

# imports
from spacepy import coordinates as coord
import spacepy.time as spt
from spacepy.time import Ticktock
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# one possible way to structure this is to have *.h file that includes all the 
# constants we might be interested in using

def getPhi_c(r, psi=0):
    """
    outputs the cusp angle according to the tsyganenko paper
    """ 

    # tsyganenko gives sample values for phi_1
    # under what context were these values found?
    # what we have here is the output in SM without psi
    # and GSM with psi
    phi_c0 = 0.24
    alpha_1 = 0.01287
    alpha_2 = 0.0314
    phi_1 = phi_c0 -(alpha_1*psi + alpha_2*psi**2)
    num = np.sqrt(r)
    den = np.sqrt(r + (1/(np.sin(phi_1)**2)) - 1) 
    phi_c = num/den + psi
    return phi_c


def tsygCyl2Car(phi_c,r):
    """
    converts to standard rh rectangular coordinate system
    given phi_c = colatitude of cusp
    r = point of interest at the cusp
    """
    # check if r and phi_c have the same length
    if len(r) == len(phi_c):
        pass
    else:
        # the lengths must not be equal
        print("something is wrong")
    
    y = np.zeros(len(phi_c))

    # perform the coordinate transforms
    x = r*np.sin(phi_c)
    y = y
    z = r*np.cos(phi_c)
    return x,y,z

def getSmOrbit():
    """
    reads in the x,y,z coordinates (originally in GSE)
    converts them to x,y,z in SM
    """
    # df = pd.read_csv('01_Jan_2019.csv')
    df = pd.read_csv('jul_65_2.csv')
    t = df['DefaultSC.A1ModJulian'] + 29999.5
    x = df['DefaultSC.gse.X']
    y = df['DefaultSC.gse.Y']
    z = df['DefaultSC.gse.Z']
    cvals = coord.Coords([[i,j,k] for i,j,k in zip(x,y,z)],'GSE','car')

    # okay so the correct "ticks" are getting set
    cvals.ticks = Ticktock(t,'MJD')
    sm = cvals.convert('SM','car')
    return sm
    

if __name__ == "__main__":
    r = np.linspace(0,10370,365)
    phi_c = getPhi_c(r)
    print(phi_c)

    x,y,z = tsygCyl2Car(phi_c,r)

    cvals = coord.Coords([[i,j,k] for i,j,k in zip(x,y,z)], 'SM','car')

    starttime = pd.Timestamp('2019-01-01T12:00:00')
    endtime = pd.Timestamp('2020-01-01T12:00:00')
    t = np.linspace(starttime.value, endtime.value, len(x))
    print("length of t", t)
    
    # just increment julian days
    cvals.ticks = Ticktock([58484 + i for i in range(0,365)],'MJD')
    cvals_gse = cvals.convert('GSE','car')
    cvals_geo = cvals.convert('GEO','car')
    # setting arbitrary times is something i just need to know how to do
    sm = getSmOrbit()
    
    # comment the next two out for the 'original' plot
    # sm = sm.convert('GSM','car')
    # cvals = cvals.convert('GSM','car')
    ax = plt.subplot(111,projection='3d')
    # ax.plot(x,y,z,label='glorious cusp vector')

    # make unit vectors,mainly because i only care about pointing direction
    ax.plot(sm.x,sm.y,sm.z, label='sm orbit')
    ax.plot(cvals.x,cvals.y,cvals.z,'g', label='sm cusp vector')
    # ax.plot(cvals_gse.x,cvals_gse.y,cvals_gse.z,label='gse cusp vector')
    # ax.plot(cvals_geo.x,cvals_geo.y,cvals_geo.z,label='geo cusp vector')
    ax.set_xlabel('meters (x)')
    ax.set_ylabel('meters (y)')
    ax.set_zlabel('meters (z)')
    plt.title('orbit and cusp vector')
    ax.legend(loc='lower left')
    plt.show()
     
    print("phi_c",np.rad2deg(phi_c))

    
