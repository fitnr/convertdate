# -*- coding: utf-8 -*-
from math import trunc
from . import gregorian

EPOCH = 2394646.5
EPOCH_GREGORIAN_YEAR = 1844

WEEKDAYS = ("Jamál", "Kamál", "Fidál", "Idál", "Istijlál", "Istiqlál", "Jalál")


def to_jd(major, cycle, year, month, day):
    '''Determine Julian day from Bahai date'''
    gy = (361 * (major - 1)) + (19 * (cycle - 1)) + (year - 1) + EPOCH_GREGORIAN_YEAR

    if month != 20:
        m = 0
    else:
        if gregorian.leap(gy + 1):
            m = -14
        else:
            m = -15
    return gregorian.to_jd(gy, 3, 20) + (19 * (month - 1)) + m + day

def from_jd(jd):
    '''Calculate Bahai date from Julian day'''

    jd = trunc(jd) + 0.5
    g = gregorian.from_jd(jd)
    gy = g[0]

    bstarty = EPOCH_GREGORIAN_YEAR

    if jd <= gregorian.to_jd(gy, 3, 20):
        x = 1
    else:
        x = 0
    # verify this next line...
    bys = gy - (bstarty + (((gregorian.to_jd(gy, 1, 1) <= jd) and x)))

    major = trunc(bys / 361) + 1
    cycle = trunc((bys % 361) / 19) + 1
    year = (bys % 19) + 1
    days = jd - to_jd(major, cycle, year, 1, 1)
    bld = to_jd(major, cycle, year, 20, 1)

    if jd >= bld:
        month = 20
    else:
        month = trunc(days / 19) + 1
    day = int((jd + 1) - to_jd(major, cycle, year, month, 1))

    return (major, cycle, year, month, day)

def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))

def to_gregorian(year, month, day):
    return gregorian.from_jd(to_jd(year, month, day))
