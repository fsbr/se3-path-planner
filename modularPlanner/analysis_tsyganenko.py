# coding: utf-8

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
earth_radius_ax = 1.5*6371 #km
#adding the year data here so I don't have to crush my github repo
pathname = '../../data-se3-path-planner/yearData/batch2015/'
# pathname = '../../data-se3-path-planner/yearData/batch2019/'
# pathname = '../../batch2019/'
sys.path.append(pathname)



# now we are making this a function, which will be copy pasted into the tsyganenko
# library and then I'll call it from there in a notebook for presentation purposes

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
        'Oct', 'Nov', 'Dec']
# months = ['Jan', 'Jul', 'Dec']
inclinations = [i for i in  range(0,90,5)] #8 
# inclinations = inclinations[::]
months = months[::]



# In[2]:
def getColorMap(filename):

    """
    reads in a bunch of different data files and outputs the 
    colormap 
    """
    df = pd.read_csv(filename)
    # df = pd.read_csv(pathname+'65_year.csv')
    # df = pd.read_csv(pathname+'Jan65.csv')
    # df = pd.read_csv(pathname+'Jan80.csv')
    # df = pd.read_csv(pathname+'Jul65.csv')
    # df = pd.read_csv(pathname+'Jul90.csv')
    GMAT_MJD_OFFSET = 29999.5
    t = df['DefaultSC.A1ModJulian'] + GMAT_MJD_OFFSET
    x = df['DefaultSC.gse.X']
    y = df['DefaultSC.gse.Y']
    z = df['DefaultSC.gse.Z']

    spacecraft = coord.Coords([[i,j,k] for i,j,k in zip(x,y,z)], 'GSE', 'car')
    spacecraft.ticks = Ticktock(t,'MJD')
    # originally SM
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

    # okay i've looked at a couple of orbits from the GSE point of view and
    # i now think that it's okay for a zero inclined orbit WRT to the earth
    # equator to be inclined WRT to the ecliptic, but like holy moley
    # these orbits are confusing sometimes.


    # In[3]:

    # goal, plot PHI on the same plot
    xc,yc,zc = tsyg.orbitalCuspLocation(spacecraft,t)
    # originally 'SM'
    cusp_location = coord.Coords([[i,j,k] for i,j,k in zip(xc,yc,zc)], 'SM', 'car')
    cusp_location.ticks = Ticktock(t,'MJD')
    # cusp_location = cusp_location.convert('SM','car')

    # fig = plt.figure()
    # ax = fig.add_subplot(111,projection='3d')
    # if I just want to :points
    # ax.plot(spacecraft.x[:points],spacecraft.y[:points],spacecraft.z[:points])
    # ax.plot(cusp_location.x[:points], cusp_location.y[:points],cusp_location.z[:points])

    # if I want EVERYTHING
    # ax.plot(spacecraft.x,spacecraft.y, spacecraft.z)
    # ax.scatter(cusp_location.x, cusp_location.y,cusp_location.z)
    # plt.title('SM Orbit and Corresponding Cusp Location')
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')
    # ax.set_xlim3d(-earth_radius_ax, earth_radius_ax)
    # ax.set_ylim3d(-earth_radius_ax, earth_radius_ax)
    # ax.set_zlim3d(-earth_radius_ax, earth_radius_ax)
    # plt.show()
    # plt.plot(cusp_location.x,cusp_location.y)
    # plt.show()


    # In[4]:

    # plt.plot(spacecraft.x,spacecraft.z)
    # plt.plot(cusp_location.x,cusp_location.z)
    # plt.xlim([-0.5*earth_radius_ax, earth_radius_ax])
    # plt.ylim([-0.5*earth_radius_ax, earth_radius_ax])
    # plt.xlabel('x')
    # plt.ylabel('z')
    # plt.title('xz plane of the cusp model')
    # plt.show()



    # In[5]:

    # the working configuration is 'SM'
    spacecraft_sph = spacecraft.convert('SM','sph')
    cusp_location_sph = cusp_location.convert('SM','sph')


    # In[6]:

    # making the plots
    points = 10000# len(spacecraft_sph.ticks.MJD)
    lowBound = 0# 156000
    highBound = points# 166000
    # plt.plot(spacecraft_sph.ticks.MJD[lowBound:highBound],spacecraft_sph.lati[lowBound:highBound],label='sc')
    # i was doing 90 - cusp location?
    # plt.plot(cusp_location_sph.ticks.MJD[lowBound:highBound],90-cusp_location_sph.lati[lowBound:highBound],label='cusp')
    # plt.legend()
    # plt.xlabel('mjd ticks')
    # plt.ylabel('sm latitude')
    # plt.title('mjd ticks vs sm latitude (cusp and spacecraft)')
    # plt.show()


    # plt.plot(spacecraft_sph.ticks.MJD[lowBound:highBound], spacecraft_sph.long[lowBound:highBound],label='sc')
    # plt.plot(cusp_location_sph.ticks.MJD[lowBound:highBound],cusp_location_sph.long[lowBound:highBound],label='cusp')
    # plt.show()

    # modlat = 90 - cusp_location_sph.lati 
    modlat = cusp_location_sph.lati
    print("modlat",modlat)


    # In[7]:

    # count it up
    count = []
    c = 0
    for satlat,cusplat, satlon,cusplon in zip(spacecraft_sph.lati, modlat, spacecraft_sph.long, cusp_location_sph.long):
        # 0<cusplon<180 i think i need a way to ensure that I'm looking at the dayside 
        # bear in mind that these bounds WILL ONLY WORK in earth - sun line centered coordinate systems
        if abs(satlat - cusplat)<=4 and abs(satlon-cusplon)<=4:
            # right now i'm using +/- 2 deg for the latitude,
            # and +/- 2 deg for the longitude
            c+=1
            count.append(c)
        else:
            count.append(c)
            
    # plt.plot(spacecraft_sph.ticks.MJD, count)
    # plt.xlabel('MJD tick')
    # plt.ylabel('cusp crossings')
    # plt.title('Cusp Crossings vs. MJD ticks')
    #plt.xlim([58700, 58800])
    # plt.show()
    print("final crossings count = ",c)

    # mean latitude of the cusp 
    print("mean sm lat of cusp", 90 - sum(cusp_location_sph.lati)/len(cusp_location_sph.lati))
    print("mean sm lon of cusp", sum(cusp_location_sph.long)/len(cusp_location_sph.long))


    # In[8]:

    # lets' see if we can check the psi function before 1pm
    r = 1.127
    psi = tsyg.getTilt(t)
    psi = np.asarray(psi)
    phic = tsyg.getPhi_c(r,psi)
    # plt.plot(phic)
    # plt.title('plot of phi_c for troubleshooting')
    # plt.show()

    # show the date in UTC
    print("UTC date", spacecraft_sph.ticks.UTC)
    return c

cma2  =[[getColorMap(pathname+month+str(inclination)+'_results.csv') for month in months[::] ] for inclination in inclinations] 
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
