# -*- coding: utf-8 -*-
from math import trunc
from utils import amod
import gregorian

EPOCH = 584282.5
HAAB_MONTHS = ("Pop", "Wo'", "Zip", "Sotz'", "Sek", "Xul",
               "Yaxk'in'", "Mol", "Ch'en", "Yax", "Sak'", "Keh",
               "Mak", "K'ank'in", "Muwan'", "Pax", "K'ayab", "Kumk'u", "Wayeb'")

TZOLKIN_MONTHS = ("Imix'", "Ik'", "Ak'b'al", "K'an", "Chikchan",
                  "Kimi", "Manik'", "Lamat", "Muluk", "Ok",
                  "Chuwen", "Eb'", "B'en", "Ix", "Men",
                  "K'ib'", "Kab'an", "Etz'nab'", "KawaK", "Ajaw")


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
    lcount = jd - EPOCH
    day = (lcount + 8 + (17 * 20)) % 365

    if day > 360:
        count = day - 360
        month = 13
    else:
        count = trunc(day / 20) + 1
        month = int((day % 20))

    return count, HAAB_MONTHS[month]


def to_tzolkin(jd):
    '''Determine Mayan Tzolkin "month" and day from Julian day'''
    lcount = jd - EPOCH
    day = int(amod(lcount + 20, 20))
    month = TZOLKIN_MONTHS[int(amod(lcount + 4, 13)) - 1]
    return day, month

