# -*- coding: utf-8 -*-
from babylonian_data import *

MONTHS = {
    1: u"Nisānu",
    2: u"Āru",
    3: u"Simanu",
    4: u"Dumuzu",
    5: u'Abu',
    6: u"Ulūlu",
    7: u"Tišritum",
    8: u"Samna",
    9: u"Kislimu",
    10: u"Ṭebētum",
    11: u"Šabaṭu",
    12: u"Addaru",
    13: u"Ulūlu II",
    14: u"Addaru II",
}

INTERCALARY = u"Makaruša"


def regnalyear(by):
    '''Determine regnal year'''
    if (by < -436):
        return

    key = max([r for r in rulers if r <= by])
    regnalyear = by - key + 1
    rulername = rulers[key]

    if (rulername == 'Alexander III [the Great]'):
        regnalyear = regnalyear + 6

    if (rulername == "Philip III Arrhidaeus"):
        regnalyear = regnalyear + 1

    if (rulername == 'Alexander IV Aegus'):
        regnalyear = regnalyear + 1

    return (regnalyear, rulername)


def arsacid_year(by):
    if (by > 64):
        return by - 64


def month_length(i):
    return lunation_periods[i] - lunation_periods[i - 1]


def from_jd(cjdn):
    '''Calculate Babylonian date from Julian Day Count'''
    if (cjdn < 1492871 or cjdn > 1748872):
        raise IndexError

    # the CJDNs of the start of the lunations in the babylonian lunar calendar are stored in 'babycal_dat'
    pd = [lu for lu in lunations if lu < cjdn and lu + 31 > cjdn].pop()
    by, bm  = lunations[pd]

    bd = cjdn - pd + 1

    # document.calendar.bmonth.selectedIndex            = bm-1

    # compute and output the date in the babylonian lunar calendar
    # bln = 1498 + i
    # document.calendar.blunnum.value                   = bln
    # document.calendar.bmlength.value                  = bml

    return (bd, MONTHS[bm], by)


def to_jd(year, month, day):
    key = [key for key, val in lunations.items() if val[0] == year and val[1] == month].pop()
    return key + day - 1



