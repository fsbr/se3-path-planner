
# coding: utf-8

# In this file, I try yet again to make a very simple cusp model.  After that, I will try to expand it.  This cusp model will literally be the simplest model possible that also includes dipole tilt.
# 
# $\phi_{cusp} = \phi_{0} + \psi$.
# 
# Then, I'll build up the model a little bit more and a little bit more etc.
# 
# I'll use the Niehoff model for the dipole tilt.  I'll use $phi_{0} = 0.24 rad \sim 78^{\circ}$
# 
# Things to consider.  
# 
# 1.  Datatypes.  Just make everything a np.array()
# 2.  The truth is the cusp model is a polar function so the MIDPOINT of the cusp may not be exactly what it's predicting.  But the other truth is, even after a few months of trying to understand this, I still feel like I don't fully understand it.
# 
# 
# 

# In[1]:

import tsyganenko as tsyg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from spacepy import coordinates as coord
import spacepy.time as spt
from spacepy.time import Ticktock
import datetime as dt
from mpl_toolkits.mplot3d import Axes3D
import sys
Re = 6371
earth_radius_ax = 1.5*Re #km
#adding the year data here so I don't have to crush my github repo
pathname = '../../data-se3-path-planner/yearData/batch2015/'
# pathname = '../../batch2019/'
sys.path.append(pathname)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
inclinations = [i for i in range(55,90,5)]

# In[2]:
def getColorMapSimple(filename):
    df = pd.read_csv(filename)
    GMAT_MJD_OFFSET = 29999.5
    t = df['DefaultSC.A1ModJulian'] + GMAT_MJD_OFFSET
    x = df['DefaultSC.gse.X']
    y = df['DefaultSC.gse.Y']
    z = df['DefaultSC.gse.Z']

    #
    xa = np.array(x)
    ya = np.array(y)
    za = np.array(z)
    print(za)
    ta = np.array(t)

    spacecraft = coord.Coords([[i,j,k] for i,j,k in zip(x,y,z)], 'GSE', 'car')
    spacecraft.ticks = Ticktock(t,'MJD')
    spacecraft = spacecraft.convert('SM','car')
    points = 10000
    # this figure validates what I already expected
    # fig = plt.figure()
    # ax = fig.add_subplot(111,projection='3d')
    # ax.plot(spacecraft.x[:points],spacecraft.y[:points],spacecraft.z[:points])
    # plt.title('SM Orbit')
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')
    # plt.show()


    # In[3]:

    # this is the part where I actually do it

    phi_0 = 0.24

    psi = tsyg.getTilt(t)

    # dude if i made a parthenthetical error like this ill be really sad

    # plt.plot(spacecraft.ticks.MJD, 90 - (phi_0 + psi))
    # plt.show()


    # In[4]:

    r = np.sqrt(xa**2 + ya**2 + za**2)/Re
    print("r equals to",r)
    phi_c = np.rad2deg(  np.arcsin((np.sqrt(r))/(np.sqrt(r + (1/np.sin(0.24))**2 - 1)))   ) +psi
    #phi = 90-(phi+psi)
    lat = 90 - phi_c
    lon = np.array(np.zeros(len(spacecraft.ticks.MJD)))
    print(lon)
    # plt.plot(t,lat)
    # plt.title('Cusp Latitude vs. MJD day')
    # plt.xlabel('MJD Day')
    # plt.ylabel('Cusp Lat, Deg')
    # plt.show()


    # In[5]:

    # LATITUDE

    #working config SM
    spacecraft_sm = spacecraft.convert('GSM','sph')
    # plt.plot(spacecraft_sm.ticks.MJD, spacecraft_sm.lati)
    # plt.plot(spacecraft_sm.ticks.MJD, lat)
    # plt.title('Spacecraft Lat and Cusp Latitude vs MJD time')
    # plt.show()





    # In[6]:

    # LONGITUDE

    # try to avoid using the [:points] way except for spot checking
    # kind of interested in a macro effect

    # plt.plot(spacecraft_sm.ticks.MJD, spacecraft_sm.long)
    # plt.plot(spacecraft_sm.ticks.MJD, lon)
    # plt.title('Spacecraft and Cusp Longitude vs. Time')
    # plt.show()


    # In[7]:

    count = []
    c = 0
    for satlat,cusplat, satlon,cusplon in zip(spacecraft_sm.lati, lat, spacecraft_sm.long, lon):
        # 0<=cusplon<180
        if abs(satlat - cusplat)<=4 and abs(satlon-cusplon)<=4:
            # right now i'm using +/- 2 deg for the latitude,
            # and +/- 2 deg for the longitude
            c+=1
            count.append(c)
        else:
            count.append(c)
            
    # plt.plot(spacecraft_sm.ticks.MJD, count)
    # plt.xlabel('MJD tick')
    # plt.ylabel('cusp crossings')
    # plt.title('Cusp Crossings vs. MJD ticks')
    #plt.xlim([58700, 58800])
    # plt.show()
    print("cusp crossings",c)
    return c

cma2 = [[getColorMapSimple(pathname+month+str(inclination)+'_results.csv') for month in months] for inclination in inclinations]

if __name__ == "__main__":
    # cdict = {'red': ((0.0, 0.0, 0.0),
    #                  (0.5, 1.0, 0.7),
    #                  (1.0, 1.0, 1.0)),
    #          'green': ((0.0, 0.0, 0.0),
    #                    (0.5, 1.0, 0.0),
    #                    (1.0, 1.0, 1.0)),
    #          'blue': ((0.0, 0.0, 0.0),
    #                   (0.5, 1.0, 0.0),
    #                   (1.0, 0.5, 1.0))}

    cdict = {'red': ((0.0, 0.0, 0.0),
                     (0.1, 0.5, 0.5),
                     (0.2, 0.0, 0.0),
                     (0.4, 0.2, 0.2),
                     (0.6, 0.0, 0.0),
                     (0.8, 1.0, 1.0),
                     (1.0, 1.0, 1.0)),
            'green':((0.0, 0.0, 0.0),
                     (0.1, 0.0, 0.0),
                     (0.2, 0.0, 0.0),
                     (0.4, 1.0, 1.0),
                     (0.6, 1.0, 1.0),
                     (0.8, 1.0, 1.0),
                     (1.0, 0.0, 0.0)),
            'blue': ((0.0, 0.0, 0.0),
                     (0.1, 0.5, 0.5),
                     (0.2, 1.0, 1.0),
                     (0.4, 1.0, 1.0),
                     (0.6, 0.0, 0.0),
                     (0.8, 0.0, 0.0),
                     (1.0, 0.0, 0.0))}
    my_cmap = colors.LinearSegmentedColormap('my_colormap',cdict,256)
    plt.pcolor(cma2,cmap=my_cmap)
    plt.colorbar()
    plt.xlabel('Start Month')
    # y_labels = [str(i) for i in  range(0,90,5)] #8 
    # plt.yticks(inclinations,str(inclinations)) 
    plt.ylabel('Inclinations')
    plt.title('Cusp Crossings Analysis 2015')
    plt.show()

