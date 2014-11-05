# -*- coding: utf-8 -*-
from math import trunc
from . import gregorian

J0000 = 1721424.5  # Julian date of Gregorian epoch: 0000-01-01
J1970 = 2440587.5  # Julian date at Unix epoch: 1970-01-01
JMJD = 2400000.5  # Epoch of Modified Julian Date system

JULIAN_EPOCH = 1721423.5


def leap(year):
    if year % 4 and year > 0:
        return 0
    else:
        return 3


def from_jd(jd):
    '''Calculate Julian calendar date from Julian day'''

    jd += 0.5
    z = trunc(jd)

    a = z
    b = a + 1524
    c = trunc((b - 122.1) / 365.25)
    d = trunc(365.25 * c)
    e = trunc((b - d) / 30.6001)

    if trunc(e < 14):
        month = e - 1
    else:
        month = e - 13

    if trunc(month > 2):
        year = c - 4716
    else:
        year = c - 4715

    day = b - d - trunc(30.6001 * e)

    #  If year is less than 1, subtract one to convert from
    #    a zero based date system to the common era system in
    #    which the year -1 (1 B.C.E) is followed by year 1 (1 C.E.).

    if year < 1:
        year -= 1

    return (year, month, day)


def to_jd(year, month, day):
    '''Adjust negative common era years to the zero-based notation we use.'''

    if year < 1:
        year += 1

    # Algorithm as given in Meeus, Astronomical Algorithms, Chapter 7, page 61

    if month <= 2:
        year -= 1
        month += 12

    return (trunc((365.25 * (year + 4716))) + trunc((30.6001 * (month + 1))) + day) - 1524.5

def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))

def to_gregorian(year, month, day):
    return gregorian.from_jd(to_jd(year, month, day))
