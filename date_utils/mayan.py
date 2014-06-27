# -*- coding: utf-8 -*-
from utils import amod, floor

EPOCH = 584282.5
HAAB_MONTHS = ("Pop", "Uo", "Zip", "Zotz", "Tzec", "Xul",
               "Yaxkin", "Mol", "Chen", "Yax", "Zac", "Ceh",
               "Mac", "Kankin", "Muan", "Pax", "Kayab", "Cumku")

TZOLKIN_MONTHS = ("Imix", "Ik", "Akbal", "Kan", "Chicchan",
                  "Cimi", "Manik", "Lamat", "Muluc", "Oc",
                  "Chuen", "Eb", "Ben", "Ix", "Men",
                  "Cib", "Caban", "Etxnab", "Cauac", "Ahau")


def to_jd(baktun, katun, tun, uinal, kin):
    '''Determine Julian day from Mayan long count'''
    return EPOCH + (baktun * 144000) + (katun * 7200) + (tun * 360) + (uinal * 20) + kin


def from_jd(jd):
    '''Calculate Mayan long count from Julian day'''
    d = jd - EPOCH
    baktun = floor(d / 144000)
    d = (d % 144000)
    katun = floor(d / 7200)
    d = (d % 7200)
    tun = floor(d / 360)
    d = (d % 360)
    uinal = floor(d / 20)
    kin = int((d % 20))

    return (baktun, katun, tun, uinal, kin)


def to_haab(jd):
    '''Determine Mayan Haab "month" and day from Julian day'''
    lcount = jd - EPOCH
    day = (lcount + 8 + ((18 - 1) * 20) % 365)

    return (floor(day / 20) + 1, int((day % 20)))


def to_tzolkin(jd):
    '''Determine Mayan Tzolkin "month" and day from Julian day'''
    lcount = jd - EPOCH
    return (int(amod(lcount + 20, 20)), int(amod(lcount + 4, 13)))

