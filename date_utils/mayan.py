# -*- coding: utf-8 -*-
from math import trunc
from utils import amod
import gregorian

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

TZOLKIN_TRANSLATIONS = ['Water', 'Air', 'Darkness', 'Net', 'Feathered Serpent', 'Death', 'Deer',
                        'Seed', 'Jade', 'Dog', 'Thread', 'Path', 'Maize', 'Tiger', 'Bird', 'Will',
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
