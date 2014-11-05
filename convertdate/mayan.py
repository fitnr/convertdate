# -*- coding: utf-8 -*-
from math import trunc
from .utils import amod
from . import gregorian

EPOCH = 584282.5
HAAB_MONTHS = ["Pop", "Wo'", "Zip", "Sotz'", "Sek", "Xul",
               "Yaxk'in'", "Mol", "Ch'en", "Yax", "Sak'", "Keh",
               "Mak", "K'ank'in", "Muwan'", "Pax", "K'ayab", "Kumk'u", "Wayeb'"]

HAAB_TRANSLATIONS = [
    "Mat", "Frog", "Red", "Bat", "Bee", "Dog", "First Sun", "Water", "Cave", "Green",
    "White", "Red", "Encloser", "Yellow Sun", "Screech Owl", "Planting Time", "Turtle", "Ripe Corn", "Nameless"]

TZOLKIN_NAMES = ["Imix'", "Ik'", "Ak'b'al", "K'an", "Chikchan",
                 "Kimi", "Manik'", "Lamat", "Muluk", "Ok",
                 "Chuwen", "Eb'", "B'en", "Ix", "Men",
                 "K'ib'", "Kab'an", "Etz'nab'", "Kawak", "Ajaw"]

TZOLKIN_TRANSLATIONS = ['Water', 'Wind', 'Darkness', 'Net', 'Feathered Serpent',
                        'Death', 'Deer', 'Seed', 'Jade', 'Dog',
                        'Thread', 'Path', 'Maize', 'Tiger', 'Bird', 'Will',
                        'Wisdom', 'Obsidian Knife', 'Thunder', 'Sun']


def to_jd(baktun, katun, tun, uinal, kin):
    '''Determine Julian day from Mayan long count'''
    return EPOCH + (baktun * 144000) + (katun * 7200) + (tun * 360) + (uinal * 20) + kin


def from_jd(jd):
    '''Calculate Mayan long count from Julian day'''
    d = jd - EPOCH
    baktun = trunc(d / 144000)
    d = (d % 144000)
    katun = trunc(d / 7200)
    d = (d % 7200)
    tun = trunc(d / 360)
    d = (d % 360)
    uinal = trunc(d / 20)
    kin = int((d % 20))

    return (baktun, katun, tun, uinal, kin)


def to_gregorian(baktun, katun, tun, uinal, kin):
    jd = to_jd(baktun, katun, tun, uinal, kin)
    return gregorian.from_jd(jd)


def from_gregorian(year, month, day):
    jd = gregorian.to_jd(year, month, day)
    return from_jd(jd)


def to_haab(jd):
    '''Determine Mayan Haab "month" and day from Julian day'''
    # Number of days since the start of the long count
    lcount = trunc(jd) + 0.5 - EPOCH
    # Long Count begins 348 days after the start of the cycle
    day = (lcount + 348) % 365

    count = day % 20
    month = trunc(day / 20)

    return int(count), HAAB_MONTHS[month]


def to_tzolkin(jd):
    '''Determine Mayan Tzolkin "month" and day from Julian day'''
    lcount = trunc(jd) + 0.5 - EPOCH
    day = amod(lcount + 4, 13)
    name = amod(lcount + 20, 20)
    return int(day), TZOLKIN_NAMES[int(name) - 1]


def lc_to_haab(baktun, katun, tun, uinal, kin):
    jd = to_jd(baktun, katun, tun, uinal, kin)
    return to_haab(jd)


def lc_to_tzolkin(baktun, katun, tun, uinal, kin):
    jd = to_jd(baktun, katun, tun, uinal, kin)
    return to_tzolkin(jd)


def lc_to_haab_tzolkin(baktun, katun, tun, uinal, kin):
    jd = to_jd(baktun, katun, tun, uinal, kin)
    dates = to_tzolkin(jd) + to_haab(jd)
    return "{0} {1} {2} {3}".format(*dates)


def translate_haab(h):
    return dict(zip(HAAB_MONTHS, HAAB_TRANSLATIONS)).get(h)


def translate_tzolkin(tz):
    return dict(zip(TZOLKIN_NAMES, TZOLKIN_TRANSLATIONS)).get(tz)


def _haab_count(day, month):
    '''Return the count of the given haab in the cycle. e.g. 0 Pop == 1, 5 Wayeb' == 365'''
    if day < 0 or day > 19:
        raise IndexError("Invalid day number")

    try:
        i = HAAB_MONTHS.index(month)
    except ValueError:
        raise ValueError("'{0}' is not a valid Haab' month".format(month))

    return min(i * 20, 360) + day


def _tzolkin_count(day, name):
    if day < 1 or day > 13:
        raise IndexError("Invalid day number")

    days = set(x + day for x in range(0, 260, 13))

    try:
        n = 1 + TZOLKIN_NAMES.index(name)
    except ValueError:
        raise ValueError("'{0}' is not a valid Tzolk'in day name".format(name))

    names = set(y + n for y in range(0, 260, 20))
    return days.intersection(names).pop()


def next_haab(haab, jd):
    '''For a given haab day, and a julian day count, find the next occurrance of that haab after the date'''
    if jd < EPOCH:
        raise IndexError("Input day is before Mayan epoch.")

    count1 = _haab_count(*to_haab(jd))
    count2 = _haab_count(*haab)

    # Find number of days between haab of given jd and desired haab
    add_days = (count2 - count1) % 365

    # add in the number of days and return new jd
    return jd + add_days


def next_tzolkin(tzolkin, jd):
    '''For a given tzolk'in day, and a julian day count, find the next occurrance of that tzolk'in after the date'''
    if jd < EPOCH:
        raise IndexError("Input day is before Mayan epoch.")

    count1 = _tzolkin_count(*to_tzolkin(jd))
    count2 = _tzolkin_count(*tzolkin)

    add_days = (count2 - count1) % 260
    return jd + add_days


def next_tzolkin_haab(tzolkin, haab, jd):
    '''For a given haab+tzolk'in combination, and a julian day count, find the next occurrance of that haab+tzolk'in after the date'''
    # get H & T of input jd, and their place in the 18,980 day cycle
    haabcount = _haab_count(*to_haab(jd))
    haab_desired_count = _haab_count(*haab)

    # How many days between the input day and the desired day?
    haab_days = (haab_desired_count - haabcount) % 365

    possible_haab = set(h + haab_days for h in range(0, 18980, 365))

    tzcount = _tzolkin_count(*to_tzolkin(jd))
    tz_desired_count = _tzolkin_count(*tzolkin)
    # How many days between the input day and the desired day?
    tzolkin_days = (tz_desired_count - tzcount) % 260

    possible_tz = set(t + tzolkin_days for t in range(0, 18980, 260))

    try:
        return possible_tz.intersection(possible_haab).pop() + jd
    except KeyError:
        raise IndexError("That Haab'-Tzolk'in combination isn't possible")
