#!/usr/bin/env python

import datetime

import numpy
import spacepy.coordinates
import spacepy.time

def tilt(t):
    """Get dipole tilt for time or range of times

    :param t: time or times to calculate tilt
    :type t: list or datetime
    :returns: positive sunward dipole tilt, in degrees, for each time
    :rtype: list
    """
    t = spacepy.time.Ticktock(t)
    c_sm = spacepy.coordinates.Coords([[0, 0, 1.0]] * len(t), 'SM', 'car',
                                      ticks=t)
    c_gsm = c_sm.convert('GSM', 'car')
    return numpy.rad2deg(numpy.arctan2(c_gsm.x, c_gsm.z))

print(tilt(spacepy.time.tickrange('2008-03-08T10:00:00', '2008-03-08T22:00:00', datetime.timedelta(hours=1))))
print(tilt(datetime.datetime(2016, 3, 3)))
print(tilt([datetime.datetime(2016, 3, 1) + datetime.timedelta(days=i)
            for i in range(7)]))
