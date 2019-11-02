# -*- coding: utf-8 -*-

# This file is part of convertdate.
# http://github.com/fitnr/convertdate

from math import trunc
from .utils import jwday, monthcalendarhelper
from . import gregorian, julian

EPOCH = 1922501.5  # beginning of proleptic year 0, day 0 of the moveable calendar
EPOCH_SARKAWAG = 2117210.5  # last day of Sarkawag's first cycle
WEEKDAYS = []
MONTHS = ["nawasard", "hoṙi", "sahmi", "trē", "kʿałocʿ", "aracʿ", "mehekan",
          "areg", "ahekan", "mareri", "margacʿ", "hroticʿ", "aweleacʿ"]
MONTHS_ARM = ["նաւասարդ", "հոռի", "սահմի", "տրէ", "քաղոց", "արաց", "մեհեկան",
              "արեգ", "ահեկան", "մարերի", "մարգաց", "հրոտից", "աւելեաց"]


def legal_date(y, m, d, method=None):
    if y < (533 if method == "sarkawag" else 1):
        raise ValueError("Year out of range for method")
    if m < 1 or d < 1:
        raise ValueError("Value out of range")
    if m > 13:
        raise ValueError("Month out of range")
    if m == 13 and d > (6 if method == "sarkawag" and leap(y) else 5):
        raise ValueError("Day out of range")
    elif d > 30:
        raise ValueError("Day out of range")
    return True


def leap(year):
    """Return true if the year was a leap year under the system of Sarkawag"""
    if year < 533:
        return False
    return year % 4 == 0


def to_jd(y, m, d, method=None):
    """Convert Armenian date to Julian day count. Use the method of Sarkawag if requested."""
    # Sanity check values
    legal_date(y, m, d, method)
    yeardays = (m - 1) * 30 + d
    if method == "sarkawag":
        # Calculate things
        yeardelta = y - 533
        leapdays = trunc(yeardelta / 4)
        return EPOCH_SARKAWAG + (365 * yeardelta) + leapdays + yeardays
    else:
        return EPOCH + (365 * y) + yeardays


def from_jd(jd, method=None):
    """Convert a Julian day count to an Armenian date. Use the method of Sarkawag if requested."""
    if method == "sarkawag":
        dc = jd - EPOCH_SARKAWAG
        if dc < 0:
            raise ValueError("Day count out of range for method")
        years = trunc(dc / 365.25)
        yeardays = dc - (365 * years + trunc(years / 4))
        if yeardays == 0:
            yeardays = 366 if years % 4 == 0 else 365
            years -= 1
        months = trunc((yeardays-1) / 30)
        days = yeardays - (30 * months)
        return years+533, months+1, trunc(days)
    else:
        dc = jd - EPOCH
        if dc < 0:
            raise ValueError("Day count out of range")
        years = trunc((dc-1) / 365)
        months = trunc(((dc-1) % 365) / 30)
        days = dc - (365 * years) - (30 * months)
        return years, months+1, trunc(days)


def to_julian(y, m, d, method=None):
    return julian.from_jd(to_jd(y, m, d, method))


def from_julian(y, m, d, method=None):
    return from_jd(julian.to_jd(y, m, d), method)


def to_gregorian(y, m, d, method=None):
    return gregorian.from_jd(to_jd(y, m, d, method))


def from_gregorian(y, m, d, method=None):
    return from_jd(gregorian.to_jd(y, m, d), method)


def month_length(y, m, method=None):
    if m > 13:
        raise ValueError("Requested month %d doesn't exist" % m)
    if m == 13:
        return 6 if (method == "sarkawag" and leap(y)) else 5
    else:
        return 30


def monthcalendar(year, month, method=None):
    start_weekday = jwday(to_jd(year, month, 1, method))
    monthlen = month_length(year, month, method)
    return monthcalendarhelper(start_weekday, monthlen)


def tostring(y, m, d, lang="en"):
    use_armenian = lang[0:2] == 'hy' or lang[0:2] == 'am' or lang == 'arm'
    return "%d %s %d" % (d, MONTHS_ARM[m-1] if use_armenian else MONTHS[m-1], y)
