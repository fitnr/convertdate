# -*- coding: utf-8 -*-
import math


def ceil(x):
    return int(math.ceil(x))


def floor(x):
    return int(math.floor(x))


def amod(a, b):
    '''Modulus function which returns numerator if modulus is zero'''
    modded = int(a % b)
    return b if modded is 0 else modded


def jwday(j):
    '''Calculate day of week from Julian day'''
    return math.trunc((j + 0.5)) % 7


def weekday_before(weekday, jd):
    return jd - jwday(jd - weekday)


# @param weekday      Day of week desired, 0 = Sunday
# @param jd           Julian date to begin search
# @param direction    1 = next weekday, -1 = last weekday
# @param offset       Offset from jd to begin search
def search_weekday(weekday, jd, direction, offset):
    '''Determine the Julian date for the next or previous weekday'''
    return weekday_before(weekday, jd + (direction * offset))


#  Utility weekday functions, just wrappers for search_weekday

def nearest_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 3)


def next_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 7)


def next_or_current_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 6)


def previous_weekday(weekday, jd):
    return search_weekday(weekday, jd, -1, 1)


def previous_or_current_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 0)


def n_weeks(weekday, jd, nthweek):
    j = 7 * nthweek

    if nthweek > 0:
        j += previous_weekday(weekday, jd)
    else:
        j += next_weekday(weekday, jd)

    return j


def monthcalendarhelper(start_weekday, month_length):
    end_weekday = start_weekday + (month_length - 1) % 7

    lpad = (start_weekday + 1) % 7
    rpad = (5 - end_weekday % 7) % 6

    days = [None] * lpad + list(range(1, 1 + month_length)) + rpad * [None]

    return [days[i:i + 7] for i in range(0, len(days), 7)]
