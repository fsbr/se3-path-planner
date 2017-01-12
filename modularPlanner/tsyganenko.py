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
Re = 6731 #km
def getTilt(t):
    """ 
    gets the dipole tilt and adds it to the tsyganenko cusp model
    almost a direct copy of J. niehof's code
    This also somewhat necessitates that we do the rest of the analysis
    in the GSM frame
    
    t = the pandas list of times (I'm assuming MJD for this use case)
    """
    t = spt.Ticktock(t,'MJD')
    c_sm = coord.Coords([[0,0,1.0]] * len(t), 'SM', 'car')
    c_sm.ticks = t
    
    # convert to gsm
    c_gsm = c_sm.convert('GSM','car')
    return np.rad2deg(np.arctan2(c_gsm.x,c_gsm.z))
    
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
    print("type(phi_c)", np.isscalar(phi_c))
    a = np.isscalar(phi_c)
    if not np.isscalar(phi_c):
        # y is probably a vector need to test
        # update i THINK it works
        y = np.zeros(len(phi_c))
    else:
        # y must be a scalar
        y = 0
    # perform the coordinate transforms
    x = r*np.sin(phi_c)
    y = y
    z = r*np.cos(phi_c)
    return x,y,z
    # return a


def getSmOrbit():
    """
    reads in the x,y,z coordinates (originally in GSE)
    converts them to x,y,z in SM
    """
    # df = pd.read_csv('01_Jan_2019.csv')
    df = pd.read_csv('oct_65_2019.csv')
    t = df['DefaultSC.A1ModJulian'] + 29999.5
    x = df['DefaultSC.gse.X']
    y = df['DefaultSC.gse.Y']
    z = df['DefaultSC.gse.Z']
    cvals = coord.Coords([[i,j,k] for i,j,k in zip(x,y,z)],'GSE','car')

    # okay so the correct "ticks" are getting set
    cvals.ticks = Ticktock(t,'MJD')
    sm = cvals.convert('SM','car')
    return sm

def orbitalCuspLocation(c,t):
    """
    returns the cusp location that corresponds with the satellites 
    actual height above the earth
    inputs: c: satellite cartesian spacepy coords object
            ticks should be instatiated a priori and the 
            t: pandas list of times
    outputs: x,y,z coordinates
    """
    
    x = c.x
    y = c.y
    z = c.z
    
    # make sure that r is in earth radii
    # this should be a list I think

    # it's also possible that these list comprehensions are WRONG
    r = [np.sqrt(i**2 + j**2 + k**2) for i,j,k in zip(x,y,z)]
    print("r euqals to",r)
    psi = [getTilt(t_i) for t_i in t]
    psi = np.asarray(psi)

    #phi_c = [getPhi_c(r_i, psi_i) for r_i,psi_i in zip(r,psi)]
    phi_c = getPhi_c(r,psi)
    print("phi_c no LC",phi_c)
    # x,y,z = [tsygCyl2Car(r_i,phi_c) for r_i, phi_c in zip(r,phi_c)]
    x = []
    y = []
    z = []
    x,y,z = tsygCyl2Car(r,phi_c)
    print("x equals to",x)
    print("y equals to",y)
    print("z equals to",z)
    return x,y,z 
    
        

if __name__ == "__main__":
    r = np.linspace(0,10370,365)
    r0 = np.linspace(0,2*6370, 365)
    phi_c0 = getPhi_c(r0)
    phi_c = getPhi_c(r)
    print(phi_c)
    plt.plot(r0,phi_c)
    plt.title('r vs phi_c')
    plt.show()
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
    sm = sm.convert('GEO','car')
    cvals = cvals.convert('GEO','car')
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
    # t = Ticktock() 
    tilts = getTilt(cvals.ticks)
    plt.plot(tilts)
    plt.show() 
     
    # trying to understand the cusp tsyganenko unit

    
