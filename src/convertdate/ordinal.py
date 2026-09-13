# -*- coding: utf-8 -*-
# This file is part of convertdate.
# http://github.com/fitnr/convertdate
# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>
"""
The `ordinal date <https://en.wikipedia.org/wiki/Ordinal_date>` specifies the day
of year as a number between 1 and 366.

Ordinal dates are represented by a tuple: ``(year, dayofyear)``
"""
from calendar import isleap
from math import trunc

from . import gregorian


def to_jd(year, dayofyear):
    '''Return Julian day count of given ordinal date.'''
    return gregorian.to_jd(year, 1, 1) + dayofyear - 1


def from_jd(jd):
    '''Convert a Julian day count to an ordinal date.

    The day of year is derived from the Gregorian date rather than the raw
    ``jd``. Both ``to_jd`` values carry the same half-day offset, so their
    difference is an exact whole number of days; subtracting ``jd`` directly
    leaves a ``.5`` remainder that ``round`` pushes the wrong way (e.g.
    ``365.5`` -> ``366``), reporting a non-existent day 366 in common years.
    '''
    year, month, day = gregorian.from_jd(jd)
    return year, int(gregorian.to_jd(year, month, day) - gregorian.to_jd(year, 1, 1)) + 1


def from_gregorian(year, month, day):
    """Convert a Gregorian date to an ordinal date."""
    m = month + 1

    if m <= 3:
        m = m + 12

    leap = isleap(year)

    t = trunc(30.6 * m) + day - 122 + 59 + leap

    if t > 365 + leap:
        t = t - 365 - leap

    return year, t


def to_gregorian(year, dayofyear):
    """Convert an ordinal date to a Gregorian date."""
    leap = isleap(year)

    if dayofyear < 59 + leap:
        leap_adj = 0
    elif leap:
        leap_adj = 1
    else:
        leap_adj = 2

    month = trunc((((dayofyear - 1 + leap_adj) * 12) + 373) / 367)

    startofmonth = from_gregorian(year, month, 1)

    return year, month, dayofyear - startofmonth[1] + 1
