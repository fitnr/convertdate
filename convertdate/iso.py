from math import trunc
from .utils import jwday, n_weeks
from . import gregorian


def to_jd(year, week, day):
    return to_julian(year, week, day)


def day_to_jd(year, day):
    return day_to_julian(year, day)


def to_julian(year, week, day):
    '''Return Julian day of given ISO year, week, and day'''
    return day + n_weeks(0, gregorian.to_jd(year - 1, 12, 28), week)


def day_to_julian(year, day):
    '''Return Julian day of given ISO year, and day of year'''
    return (day - 1) + gregorian.to_jd(year, 1, 1)


def from_jd(jd):
    '''Return tuple of ISO (year, week, day) for Julian day'''
    year = gregorian.from_jd(jd - 3)[0]
    if jd >= to_julian(year + 1, 1, 1):
        year += 1
    week = trunc((jd - to_julian(year, 1, 1)) / 7) + 1
    day = jwday(jd)
    if day == 0:
        day = 7

    return (year, week, day)


def from_jd_to_iso_day(jd):
    '''Return tuple of ISO (year, day_of_year) for Julian day'''
    year = gregorian.from_jd(jd)[0]
    day = trunc(jd - gregorian.to_jd(year, 1, 1)) + 1
    return (year, day)

