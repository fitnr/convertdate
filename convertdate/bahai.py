# -*- coding: utf-8 -*-
from math import trunc
from . import gregorian
from .utils import monthcalendarhelper, jwday

EPOCH = 2394646.5
EPOCH_GREGORIAN_YEAR = 1844

WEEKDAYS = ("Jamál", "Kamál", "Fidál", "Idál", "Istijlál", "Istiqlál", "Jalál")

MONTHS = ("Bahá", "Jalál", "Jamál", "‘Aẓamat", "Núr", "Raḥmat", "Kalimát", "Kamál", "Asmá’",
          "‘Izzat", "Mashíyyat", "‘Ilm", "Qudrat", "Qawl", "Masá’il", "Sharaf", "Sulṭán", "Mulk",
          "Ayyám-i-Há", "‘Alá")

ENGLISH_MONTHS = ("Splendor", "Glory", "Beauty", "Grandeur", "Light", "Mercy", "Words",
                  "Perfection", "Names", "Might", "Will", "Knowledge", "Power", "Speech", "Questions",
                  "Honour", "Sovereignty", "Dominion", "Days of Há", "Loftiness")


def to_jd(year, month, day):
    '''Determine Julian day from Bahai date'''
    gy = year - 1 + EPOCH_GREGORIAN_YEAR

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

    year = bys + 1
    days = jd - to_jd(year, 1, 1)
    bld = to_jd(year, 20, 1)

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
    if month == 19:
        if gregorian.leap(year + EPOCH_GREGORIAN_YEAR):
            return 5
        else:
            return 4

    else:
        return 19


def monthcalendar(year, month):
    start_weekday = jwday(to_jd(year, month, 1))
    monthlen = month_length(year, month)
    return monthcalendarhelper(start_weekday, monthlen)
