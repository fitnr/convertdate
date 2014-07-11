# -*- coding: utf-8 -*-
from math import trunc

EPOCH = 1721425.5

HAVE_30_DAYS = (4, 6, 9, 11)
HAVE_31_DAYS = (1, 3, 5, 7, 8, 10, 12)

def leap(year):
    return year % 4 == 0 and not ((year % 100) == 0 and (year % 400) != 0)

def _legal_date(year, month, day):
    if day > 31:
        raise IndexError("Day greater than 31")

    if month in HAVE_30_DAYS and day == 31:
        raise IndexError("Month {0} only has 30 days".format(month))

    if month == 2:
        daysinfeb = 29 if leap(year) else 28
        if day > daysinfeb:
            raise IndexError("February doesn't have that many days")

def to_jd(year, month, day):
    '''Gregorian to Julian Day Count for years between 1801-2099'''
    # http://quasar.as.utexas.edu/BillInfo/JulianDatesG.html

    _legal_date(year, month, day)

    if month <= 2:
        year = year - 1
        month = month + 12

    a = trunc(year / 100)
    b = trunc(a / 4)
    c = 2 - a + b
    e = trunc(365.25 * (year + 4716))
    f = trunc(30.6001 * (month + 1))
    return c + day + e + f - 1524.5

def to_jd2(year, month, day):

    _legal_date(year, month, day)

    if month <= 2:
        leap_adj = 0
    elif leap(year):
        leap_adj = -1
    else:
        leap_adj = -2

    return (
        EPOCH - 1 + (365 * (year - 1)) +
        trunc((year - 1) / 4) + (-trunc((year - 1) / 100)) +
        trunc((year - 1) / 400) + trunc((((367 * month) - 362) / 12) + leap_adj + day)
        )


def from_jd(jd):
    '''Return Gregorian date in a (Y, M, D) tuple'''
    wjd = trunc(jd - 0.5) + 0.5
    depoch = wjd - EPOCH
    quadricent = trunc(depoch / 146097)
    dqc = depoch % 146097
    cent = trunc(dqc / 36524)
    dcent = dqc % 36524
    quad = trunc(dcent / 1461)
    dquad = dcent % 1461
    yindex = trunc(dquad / 365)
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

    month = trunc((((yearday + leap_adj) * 12) + 373) / 367)

    day = int(wjd - to_jd(year, month, 1)) + 1

    return (year, month, day)

