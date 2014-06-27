# -*- coding: utf-8 -*-
from calendar_util import Julianday
from astro import floor


EPOCH = 1721425.5


def leap(year):
    return (year % 4 == 0 and not ((year % 100) == 0 and (year % 400) != 0))


def to_jd(year, month, day):
    if month <= 2:
        leap_adj = 0
    elif leap(year):
        leap_adj = -1
    else:
        leap_adj = -2

    return Julianday(
      (EPOCH - 1) + (365 * (year - 1)) + floor((year - 1) / 4) +
      (-floor((year - 1) / 100)) + floor((year - 1) / 400) +
      floor((((367 * month) - 362) / 12) + leap_adj + day)
    )


def from_jd(jd):
    '''Return Gregorian date in a (Y, M, D) tuple'''
    wjd = floor(jd - 0.5) + 0.5
    depoch = wjd - EPOCH
    quadricent = floor(depoch / 146097)
    dqc = depoch % 146097
    cent = floor(dqc / 36524)
    dcent = dqc % 36524
    quad = floor(dcent / 1461)
    dquad = dcent % 1461
    yindex = floor(dquad / 365)
    year = (quadricent * 400) + (cent * 100) + (quad * 4) + yindex
    if not (cent == 4 or yindex == 4):
        year += 1
    yearday = wjd - to_jd(year, 1, 1)
    if wjd < to_jd(year, 3, 1):
        leap_adj = 0
    elif leap(year):
        leap_adj = 1
    else:
        leap_adj = 2

    month = floor((((yearday + leap_adj) * 12) + 373) / 367)

    day = int(wjd - to_jd(year, month, 1)) + 1

    return (year, month, day)
