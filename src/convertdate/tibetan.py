# -*- coding: utf-8 -*-
# This file is part of convertdate.
# http://github.com/fitnr/convertdate
# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2022, slad2019 <snowlionandthedragon>

"""
The Tibetan calendar
"""
import math
from decimal import Decimal
from typing import Tuple, Callable
from . import gregorian

class Cal_school:
    y0: int
    m0: int
    beta_star: int

    beta: int
    gamma: int
    gamma_star: int    

    def __init__(self, y0, m0, beta_star, ix_leap=48):
        self.y0 = y0
        self.m0 = m0
        self.beta_star = beta_star
        self.ix_leap = ix_leap

        self.beta = 184 - beta_star
        self.gamma = (-y0 - 19 * self.beta) % 65
        self.gamma_star = (-24 * y0 - self.beta) % 65

        self.md1 = Decimal(167025) / Decimal(5656)
        self.md2 = Decimal(11135) / Decimal(11312)
        self.md0 = 2015501 + Decimal(4783) / Decimal(5656)

        self.s1 = Decimal(65) / Decimal(804)
        self.s2 = Decimal(13) / Decimal(4824)
        self.s0 = Decimal(743) / Decimal(804)

        self.a1 = Decimal(253) / Decimal(3528)
        self.a2 = Decimal(1) / Decimal(28)
        #self.a2 = Decimal(3781) / Decimal(105840)
        self.a0 = Decimal(475) / Decimal(3528)

        self.moon_tab = [0, 5, 10, 15, 19, 22, 24, 25]
        self.sun_tab = [0, 6, 10, 11]

sch = Cal_school(y0 = 806, m0 = 3, beta_star = 61) # phugpa

def true_month_leap(y: int, m: int) -> Tuple[int, bool]:
    '''Calculate a true month count of year/month
       Also return whether it is leap month or not
    '''
    solar_month_cnt: int = 12 * (y - sch.y0) + m - sch.m0
    true_month_rcnt: float = (67 * solar_month_cnt + sch.beta_star) / 65
    ix: int = (67 * solar_month_cnt + sch.beta_star) % 65
    if ix in [sch.ix_leap, sch.ix_leap+1]:
        leap_month = True
    else:
        leap_month = False
    
    if ix < sch.ix_leap:
        true_month_cnt = math.floor(true_month_rcnt)
    elif ix in [sch.ix_leap, sch.ix_leap+1]:
        true_month_cnt = math.floor(true_month_rcnt)
    else:
        true_month_cnt = math.ceil(true_month_rcnt)
    return(true_month_cnt, leap_month)

def mean_date(n: int, d: int):
    return(n * sch.md1 + d * sch.md2 + sch.md0) 

def mean_sun(n: int, d: int):
    return(n * sch.s1 + d * sch.s2 + sch.s0)

def anomaly_moon(n: int, d: int):
    return(n * sch.a1 + d * sch.a2 + sch.a0)

def moon_tab_int(i: int) -> int:
    k = i % 28
    if k <= 7:
        return(sch.moon_tab[k])
    elif k <= 14:
        return(sch.moon_tab[14-k])
    elif k <= 21:
        return(-sch.moon_tab[k-14])
    else:
        return(-sch.moon_tab[28-k])

def sun_tab_int(i: int):
    k = i % 12
    if k <= 3:
        return(sch.sun_tab[k])
    elif k <= 6:
        return(sch.sun_tab[6-k])
    elif k <= 9:
        return(-sch.sun_tab[k-6])
    else:
        return(-sch.sun_tab[12-k])

def tab_float(f: Callable, a: float) -> float:
    a_floor: int = math.floor(a)
    a_frac = a - a_floor
    a_tab = f(a_floor)
    a_tab_plus = f(a_floor+1)
    a_tab_float: float = a_tab + (a_tab_plus - a_tab) * a_frac
    return(a_tab_float)

def true_date(n: int, d: int):
    me = tab_float(moon_tab_int, 28 * anomaly_moon(n, d)) # moon_equ
    se = tab_float(sun_tab_int, 12 * (mean_sun(n, d) - Decimal(0.25))) # sun_equ
    td = mean_date(n, d) + Decimal(me / 60) - Decimal(se / 60)

    return(td)

def inc_lunar_day(n, d):
    if d == 30:
        n += 1
        d = 1
    else:
        d += 1
    return (n, d)

def dec_lunar_day(n, d):
    if d == 1:
        n -= 1
        d = 30
    else:
        d -= 1
    return (n, d)

def to_jd(year, month, leap_month, day, leap_day):
    '''Obtain Julian day for Tibetan date'''
    if month not in range(1, 13) or day not in range(1, 31):
        raise ValueError('Month %d or day %d out of range' % (month, day))
    (n, lm) = true_month_leap(year, month)
    if not lm and leap_month:
        raise ValueError('Year %d month %d is not a leap month.' % (year, month))
    if lm and not leap_month:
        # in tibetan calendar, leap month is first month, and regular month is following 
        # month with same number.
        n += 1  
    td = true_date(n, day)
    jd = math.floor(td)
    # check for skipped day and leap day
    ld = False
    sk = False
    td_minus = true_date(*dec_lunar_day(n, day))
    if math.floor(td_minus) == jd:
        sk = True
    if sk:
        raise ValueError('Year %d %smonth %d day %d is a skipped day' %
            (year, 'leap ' if leap_month else '', month, day))
    if math.floor(td_minus) + 2 == jd:
        ld = True
    if not ld and leap_day:
        raise ValueError('Year %d %smonth %d day %d is not a leap day' %
            (year, 'leap ' if leap_month else '', month, day))
    if ld and leap_day:
        jd -= 1

    jd -= 0.5 #adjust for midday julian date
    return (jd)

def inv_true_date(n):
    a = 65 * n + sch.beta
    x = math.ceil(a / 67)
    m = 1 + (x-1) % 12
    y = math.ceil(x/12) - 1 + sch.y0
    l = (a % 67) in [1, 2]

    return(y, m, l)

def from_jd(jd):
    '''Calculate Tibetan date from Julian day'''
    jd += 0.5 #adjust for midday julian date
    ld = False

    # first get the approx. date by mean_date
    n = math.floor((Decimal(jd) - sch.md0) / sch.md1)
    c = Decimal(jd) - sch.md0 - n * sch.md1
    d = math.floor(c / sch.md2)
    while (True):
        aprox_jd = true_date(n, d)
        if aprox_jd >= jd:
            if math.floor(aprox_jd) == jd+1:
                ld = True
            break
        else: # aprox_date < jd
            n, d = inc_lunar_day(n, d)

    (y, m, lm) = inv_true_date(n)
    return(y, m, lm, d, ld)

def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))


def to_gregorian(year, month, leap_month, day, leap_day):
    return gregorian.from_jd(to_jd(year, month, leap_month, day, leap_day))

def jd_of_day1(year, month, leap_month):

    (n, lm) = true_month_leap(year, month)
    if not lm and leap_month:
        raise ValueError('Year %d month %d is not a leap month.' % (year, month))
    if lm and not leap_month:
        # in tibetan calendar, leap month is first month, and regular month is following 
        # month with same number.
        n += 1

    jd1 = to_jd(year, month, leap_month, day=1, leap_day=False)
  
    td_minus = true_date(*dec_lunar_day(n, 1))
    if math.floor(td_minus) == jd1:
        sk = True
    else:
        sk = False
    if math.floor(td_minus) + 2 == jd1:
        ld = True
    else:
        ld = False
    # if 1 is leap day, the first day is (1, leap_day=True) with jd1-1
    if ld:
        jd1 -= 1
    # if 1 is skipped day, the first day is 2, with jd1+1
    if sk:
        jd1 += 1
    return(jd1)

def month_length(year, month, leap_month):
    jd1 = jd_of_day1(year, month, leap_month)
    jd2 = to_jd(year, month, leap_month, day=30, leap_day=False)
    # if 30 is skip day, its jd is same
    # if 30 is leap day, (30, leap_day=False) is last day

    return(jd2 - jd1 + 1)

def monthcalendar(year, month, leap_month):
    start_weekday = jwday(jd_of_day1(year, month, leap_month))
    monthlen = month_length(year, month, leap_month)
    return monthcalendarhelper(start_weekday, monthlen)


def format(year, month, day):
    """Convert a Tibetan date into a string with the format DD MONTH YYYY."""
