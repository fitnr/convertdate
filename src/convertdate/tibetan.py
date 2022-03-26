# -*- coding: utf-8 -*-
# This file is part of convertdate.
# http://github.com/fitnr/convertdate
# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2022, slad2019 <snowlionandthedragon>
"""
The Tibetan calendar

Based on 'Tibetan calendar mathematics', 2nd ed., 2014, arXiv: 1401.6285.
Tibetan calendar a luni-solar calendar based on Indian's Kalacakra Calendar system.
There are several versions with different epoch data. This implementation is
the most popular Phugpa version, which was officially introduced by the Tibet ruler
Drogön Chögyal Phagpa in the 13th century. The Phugpa calendar has been reformed several
times and now is widely used in Tibet.

Tibetan Calendar has 12 or 13 months per year, 29 or 30 days per month. It has leap month
and leap day, also skipped day.

TODO:
    add month calendar, as Tibetan calendar has leap day and skipped day, it can't use the
    monthcalendarhelper to output calendar.
"""
import math
from decimal import Decimal
from typing import Tuple, Callable
from . import gregorian


PHUGPHA_BETA_STAR = 61
PHUGPHA_Y0 = 806
PHUGPHA = dict(
    y0=PHUGPHA_Y0,
    m0=3,
    beta_star=PHUGPHA_BETA_STAR,
    beta=184 - PHUGPHA_BETA_STAR,
    ix_leap=48,
    gamma=(-PHUGPHA_Y0 - 19 * (184 - PHUGPHA_BETA_STAR)) % 65,
    gamma_star=(-24 * PHUGPHA_Y0 - (184 - PHUGPHA_BETA_STAR)) % 65,
    md1=167025 / Decimal(5656),
    md2=11135 / Decimal(11312),
    md0=2015501 + 4783 / Decimal(5656),
    s1=65 / Decimal(804),
    s2=13 / Decimal(4824),
    s0=743 / Decimal(804),
    a1=253 / Decimal(3528),
    a2=1 / Decimal(28),
    a0=475 / Decimal(3528),
    moon_tab=[0, 5, 10, 15, 19, 22, 24, 25],
    sun_tab=[0, 6, 10, 11],
)


def true_month_leap(y: int, m: int, method=None) -> Tuple[int, bool]:
    """Calculate a true month count of year/month
    Also return whether it is leap month or not
    """
    school = method or PHUGPHA
    solar_month_cnt: int = 12 * (y - school["y0"]) + m - school["m0"]
    true_month_rcnt: float = (67 * solar_month_cnt + school["beta_star"]) / 65
    ix: int = (67 * solar_month_cnt + school["beta_star"]) % 65

    leap_month = ix in [school["ix_leap"], school["ix_leap"] + 1]

    if ix < school["ix_leap"]:
        true_month_cnt = math.floor(true_month_rcnt)
    elif ix in [school["ix_leap"], school["ix_leap"] + 1]:
        true_month_cnt = math.floor(true_month_rcnt)
    else:
        true_month_cnt = math.ceil(true_month_rcnt)
    return true_month_cnt, leap_month


def mean_date(n: int, d: int, method=None):
    school = method or PHUGPHA
    return n * school["md1"] + d * school["md2"] + school["md0"]


def mean_sun(n: int, d: int, method=None):
    school = method or PHUGPHA
    return n * school["s1"] + d * school["s2"] + school["s0"]


def anomaly_moon(n: int, d: int, method=None):
    school = method or PHUGPHA
    return n * school["a1"] + d * school["a2"] + school["a0"]


def moon_tab_int(i: int, method=None) -> int:
    school = method or PHUGPHA
    k = i % 28
    if k <= 7:
        return school["moon_tab"][k]
    if k <= 14:
        return school["moon_tab"][14 - k]
    if k <= 21:
        return -school["moon_tab"][k - 14]

    return -school["moon_tab"][28 - k]


def sun_tab_int(i: int, method=None):
    school = method or PHUGPHA
    k = i % 12
    if k <= 3:
        return school["sun_tab"][k]
    if k <= 6:
        return school["sun_tab"][6 - k]
    if k <= 9:
        return -school["sun_tab"][k - 6]
    return -school["sun_tab"][12 - k]


def tab_float(f: Callable, a: float) -> float:
    a_floor: int = math.floor(a)
    a_frac = a - a_floor
    a_tab = f(a_floor)
    a_tab_plus = f(a_floor + 1)
    a_tab_float: float = a_tab + (a_tab_plus - a_tab) * a_frac
    return a_tab_float


def true_date(n: int, d: int, method=None):
    me = tab_float(moon_tab_int, 28 * anomaly_moon(n, d, method))  # moon_equ
    se = tab_float(sun_tab_int, 12 * (mean_sun(n, d, method) - Decimal(0.25)))  # sun_equ
    td = mean_date(n, d) + Decimal(me / 60) - Decimal(se / 60)
    return td


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


def to_jd(year, month, leap_month, day, leap_day, method=None):
    '''Obtain Julian day for Tibetan date'''
    if month not in range(1, 13) or day not in range(1, 31):
        raise ValueError(f"Month {month} or day {day} out of range")

    n, lm = true_month_leap(year, month)

    if not lm and leap_month:
        raise ValueError(f"Year {year} month {month} is not a leap month")

    if lm and not leap_month:
        # in tibetan calendar, leap month is first month, and regular month is following
        # month with same number.
        n += 1
    td = true_date(n, day, method)
    jd = math.floor(td)
    # check for skipped day and leap day
    td_minus = true_date(*dec_lunar_day(n, day))
    if math.floor(td_minus) == jd:
        raise ValueError(
            "Year %d %s month %d day %d is a skipped day" % (year, 'leap ' if leap_month else '', month, day)
        )

    is_leap = math.floor(td_minus) + 2 == jd
    if not is_leap and leap_day:
        raise ValueError(
            "Year %d %s month %d day %d is not a leap day" % (year, 'leap ' if leap_month else '', month, day)
        )
    if is_leap and leap_day:
        jd -= 1

    jd -= 0.5  # adjust for midday julian date
    return jd


def inv_true_date(n, method=None):
    school = method or PHUGPHA
    a = 65 * n + school["beta"]
    x = math.ceil(a / 67)
    m = 1 + (x - 1) % 12
    y = math.ceil(x / 12) - 1 + school["y0"]
    l = (a % 67) in [1, 2]

    return (y, m, l)


def from_jd(jd, method=None):
    '''Calculate Tibetan date from Julian day'''
    school = method or PHUGPHA
    jd += 0.5  # adjust for midday julian date
    ld = False

    # first get the approx. date by mean_date
    n = math.floor((Decimal(jd) - school["md0"]) / school["md1"])
    c = Decimal(jd) - school["md0"] - n * school["md1"]
    d = math.floor(c / school["md2"])
    while True:
        aprox_jd = true_date(n, d, method=school)
        if aprox_jd >= jd:
            if math.floor(aprox_jd) == jd + 1:
                ld = True
            break

        # aprox_date < jd
        n, d = inc_lunar_day(n, d)

    (y, m, lm) = inv_true_date(n, method=school)
    return (y, m, lm, d, ld)


def from_gregorian(year, month, day, method=None):
    return from_jd(gregorian.to_jd(year, month, day), method)


def to_gregorian(year, month, leap_month, day, leap_day, method=None):
    return gregorian.from_jd(to_jd(year, month, leap_month, day, leap_day, method))


def jd_of_day1(year, month, leap_month, method=None):
    n, lm = true_month_leap(year, month, method)
    if not lm and leap_month:
        raise ValueError(f"Year {year} month {month} is not a leap month.")
    if lm and not leap_month:
        # in tibetan calendar, leap month is first month, and regular month is following
        # month with same number.
        n += 1

    jd1 = to_jd(year, month, leap_month, day=1, leap_day=False, method=method)

    td_minus = true_date(*dec_lunar_day(n, 1))
    # if 1 is leap day, the first day is (1, leap_day=True) with jd1-1
    if math.floor(td_minus) + 2 == jd1:
        jd1 -= 1
    # if 1 is skipped day, the first day is 2, with jd1+1
    if math.floor(td_minus) == jd1:
        jd1 += 1
    return jd1


def month_length(year, month, leap_month, method=None):
    jd1 = jd_of_day1(year, month, leap_month, method)
    jd2 = to_jd(year, month, leap_month, day=30, leap_day=False, method=method)
    # if 30 is skip day, its jd is same
    # if 30 is leap day, (30, leap_day=False) is last day

    return jd2 - jd1 + 1
