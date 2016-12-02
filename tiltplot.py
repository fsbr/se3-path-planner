import numpy as np
import datetime
import spacepy.time
import spacepy.coordinates
import matplotlib.pyplot as plt
def tilt(t):
    # Get dipole tilt for time or range of times
    # :param t: time or times to calculate tilt
    # :type t: list or datetime
    # :returns: positive sunward dipole tilt, in degrees, for each time
    # :rtype: list
    t = spacepy.time.Ticktock(t)
    c_sm = spacepy.coordinates.Coords([[0, 0, 1.0]] * len(t), 'SM', 'car',
                                      ticks=t)
    c_gsm = c_sm.convert('GSM', 'car')

    return np.rad2deg(np.arctan2(c_gsm.x, c_gsm.z))

tilts=tilt(spacepy.time.tickrange('2016-01-01T00:00:00', '2017-01-01T00:00:00', datetime.timedelta(hours=24)))
print("tilts", tilts)
plt.plot(tilts)
plt.xlabel('Day of Year')
plt.ylabel('Dipole Tilt (degrees)') 
plt.title('Magnetic Dipole Tilt as Function of Time')
plt.show()
