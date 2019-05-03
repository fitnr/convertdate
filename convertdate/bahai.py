#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>
from math import trunc
from calendar import isleap
from . import gregorian
from .utils import monthcalendarhelper, jwday
from pymeeus.Sun import Sun
from pymeeus.Epoch import Epoch
from pymeeus.Angle import Angle


EPOCH = 2394646.5
EPOCH_GREGORIAN_YEAR = 1844

WEEKDAYS = ("Jamál", "Kamál", "Fidál", "Idál", "Istijlál", "Istiqlál", "Jalál")

MONTHS = ("Bahá", "Jalál", "Jamál", "‘Aẓamat", "Núr", "Raḥmat", "Kalimát", "Kamál", "Asmá’",
          "‘Izzat", "Mashíyyat", "‘Ilm", "Qudrat", "Qawl", "Masá’il", "Sharaf", "Sulṭán", "Mulk",
          "Ayyám-i-Há", "‘Alá")

ENGLISH_MONTHS = ("Splendor", "Glory", "Beauty", "Grandeur", "Light", "Mercy", "Words",
                  "Perfection", "Names", "Might", "Will", "Knowledge", "Power", "Speech", "Questions",
                  "Honour", "Sovereignty", "Dominion", "Days of Há", "Loftiness")

def gregorian_day_of_nawruz(year):
    
    if year == 2059:
        return 20

    # get time of spring equinox
    equinox = Sun.get_equinox_solstice(year, "spring")

    # get sunset times in Tehran
    latitude = Angle(35.6944)
    longitude = Angle(51.4215)

    # get time of sunset in Tehran
    days = [19,20,21]
    sunsets = list(map(lambda x: Epoch(year, 3, x).rise_set(latitude, longitude)[1], days))

    # compare
    if equinox < sunsets[1]:
        if equinox < sunsets[0]:
            return 19
        else:
            return 20
    else:
        if equinox < sunsets[2]:
            return 21
        else:
            return 22

def to_jd(year, month, day):
    '''Determine Julian day from Bahai date'''

    if month <= 18:
        gy = year - 1 + EPOCH_GREGORIAN_YEAR
        nawruz_day = gregorian_day_of_nawruz(gy)
        return gregorian.to_jd(gy, 3, nawruz_day - 1) + day + (month-1)*19

    else:
        return self.to_jd(year, month - 1, day) + self.month_length(year, month)


def from_jd(jd):
    '''Calculate Bahai date from Julian day'''

    jd = trunc(jd) + 0.5
    g = gregorian.from_jd(jd)
    gy = g[0]
    nawruz_day = gregorian_day_of_nawruz(gy)

    bstarty = EPOCH_GREGORIAN_YEAR

    if jd <= gregorian.to_jd(gy, 3, 20):
        x = 1
    else:
        x = 0
    # verify this next line...
    bys = gy - (bstarty + (((gregorian.to_jd(gy, 1, 1) <= jd) and x)))

    year = bys + 1
    days = jd - to_jd(year, 1, 1)
    bld = to_jd(year, nawruz_day - 1, 1)

    if jd >= bld:
        month = 20
    else:
        month = trunc(days / 19) + 1
    day = int((jd + 1) - to_jd(year, month, 1))

    return year, month, day


def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))


def to_gregorian(year, month, day):
    return gregorian.from_jd(to_jd(year, month, day))


def month_length(year, month):
    gy = year + EPOCH_GREGORIAN_YEAR - 1

    if month == 19:
        nawruz_future = gregorian_day_of_nawruz(gy+1)
        nawruz_past = gregorian_day_of_nawruz(gy)
        length_of_year = nawruz_future+365-nawruz_past

        if isleap(gy+1):
            length_of_year = length_of_year + 1
        return length_of_year - 19*19

    else:
        return 19


def monthcalendar(year, month):
    start_weekday = jwday(to_jd(year, month, 1))
    monthlen = month_length(year, month)
    return monthcalendarhelper(start_weekday, monthlen)
