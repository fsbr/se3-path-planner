# What I"m trying to do here is program the tysganenko model so that the plots actually
# look something like they do in the tsyganenko paper.
# I really want to have this done by monday but we will see
# tckf jan 2017

# imports
from spacepy import coordinates as coord
from spacepy.time import Ticktock
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# one possible way to structure this is to have *.h file that includes all the 
# constants we might be interested in using

def getPhi_c(r, psi=0):
    """
    outputs the cusp angle
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
    # not sure but i think i need to have r = 1 easy to just comment out
    # r = 1
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

if __name__ == "__main__":
    r = np.linspace(0,637000,10000)
    phi_c = getPhi_c(r)
    print(phi_c)

    x,y,z = tsygCyl2Car(phi_c,r)
    ax = plt.subplot(111,projection='3d')
    ax.plot(x,y,z,label='glorious cusp vector')
    ax.legend()
    plt.show()
     
    print("phi_c",np.rad2deg(phi_c))
