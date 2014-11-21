# -*- coding: utf-8 -*-
from math import trunc
from . import dublin, gregorian, utils
import ephem

EPOCH = 2375839.5

YEAR_EPOCH = 1791

MOIS = [
    'Vendémiaire',
    'Brumaire',
    'Frimaire',
    'Nivôse',
    'Pluviôse',
    'Ventôse',
    'Germinal',
    'Floréal',
    'Prairial',
    'Messidor',
    'Thermidor',
    'Fructidor'
]


def leap(year, method=100):
    '''Determine if this is a leap year in the FR calendar using one of three methods: 4, 100, 128
    (every 4th years, every 4th or 400th but not 100th, every 4th but not 128th)'''

    if year in (3, 7, 11, 15):
        return True
    elif year < 20:
        return False

    if method == 4:
        return year % 4 == 3

    elif (method == 100):
        return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

    elif method == 128:
        return year % 4 == 0 and year % 128 != 0


def premier_da_la_annee(jd):
    '''Determine the year in the French revolutionary calendar in which a given Julian day falls.
    Returns Julian day number containing fall equinox (first day of the FR year)'''
    e = ephem.previous_fall_equinox(dublin.from_jd(jd))
    return trunc(dublin.to_jd(e) - 0.5) + 0.5


def to_jd(an, mois, jour):
    '''Obtain Julian day from a given French Revolutionary calendar date.'''
    day_of_adr = (30 * (mois - 1)) + (jour - 1)
    equinoxe = ephem.next_fall_equinox(str(an + YEAR_EPOCH))
    return trunc(dublin.to_jd(equinoxe.real) - 0.5) + 0.5 + day_of_adr


def from_jd(jd):
    '''Calculate date in the French Revolutionary
    calendar from Julian day.  The five or six
    "sansculottides" are considered a thirteenth
    month in the results of this function.'''
    jd = trunc(jd) + 0.5
    equinoxe = premier_da_la_annee(jd)

    an = gregorian.from_jd(equinoxe)[0] - YEAR_EPOCH
    mois = trunc((jd - equinoxe) / 30) + 1
    jour = int((jd - equinoxe) % 30) + 1

    return (an, mois, jour)


def decade(jour):
    return trunc(jour / 10) + 1


def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))


def to_gregorian(an, mois, jour):
    return gregorian.from_jd(to_jd(an, mois, jour))


def format(an, mois, jour):
    return "{0} {1} {2}".format(jour, MOIS[mois - 1], an)
