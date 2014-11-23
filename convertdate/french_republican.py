# -*- coding: utf-8 -*-
from math import trunc
from . import dublin, gregorian
from .data.french_republican_days import french_republican_days
import ephem

EPOCH = 2375839.5

YEAR_EPOCH = 1791

DAYS_IN_YEAR = 365

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
    'Fructidor',
    'Sansculottides'
]

LEAP_CYCLE_DAYS = 1461  # 365 * 4 + 1
LEAP_CYCLE_YEARS = 4

# methods:
# 4: leap every four years: 3, 7, 11, etc
# 100: leap every 4th and 400th year, but not 100th: 20, 24, ... 96, 104, ... 396, 400, ...
# 128: leap every 4th but not 128th: 20, 24, ... 124, 132, ...
# equinox: [default] use calculation of the equinox to determine date, never returns a leap year


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

    return False


def premier_da_la_annee(jd):
    '''Determine the year in the French revolutionary calendar in which a given Julian day falls.
    Returns Julian day number containing fall equinox (first day of the FR year)'''
    e = ephem.previous_fall_equinox(dublin.from_jd(jd))
    return trunc(dublin.to_jd(e) - 0.5) + 0.5


def to_jd(year, month, day, method=None):
    '''Obtain Julian day from a given French Revolutionary calendar date.'''
    method = method or 'equinox'

    if method == 'equinox':
        return _to_jd_equinox(year, month, day,)

    else:
        return _to_jd_schematic(year, month, day, method)


def _to_jd_schematic(year, month, day, method):
    '''Calculate JD with a variety of methods'''

    if method == 4:
        # these are ignored
        intercal_cycle_days = leap_suppression_days = 1
        intercal_cycle_yrs = leap_suppression_yrs = None

    elif method == 100:
        leap_suppression_yrs = 100
        leap_suppression_days = 36524  # leap_cycle_days * 25 - 1
        intercal_cycle_yrs = 400
        intercal_cycle_days = 146097  # leap_suppression_days * 3 + leap_cycle_days * 25

    elif method == 128:
        leap_suppression_days = 46751  # 32 * 1461 - 1
        intercal_cycle_yrs = leap_suppression_yrs = 128
        intercal_cycle_days = 46751  # 31 + 128 * 365

    else:
        raise ValueError("Unknown leap year method. Try: 4, 100, 128")

    if intercal_cycle_yrs:
        y0 = trunc(year / intercal_cycle_yrs)
        year = year - y0 * intercal_cycle_yrs
    else:
        y0 = 0

    if leap_suppression_yrs:
        y1 = trunc(year / leap_suppression_yrs)
        year = year - y1 * leap_suppression_yrs
    else:
        y1 = 0

    y2 = trunc(year / LEAP_CYCLE_YEARS)
    year = year - y2 * LEAP_CYCLE_YEARS

    yj = (
        y0 * intercal_cycle_days +
        y1 * leap_suppression_days +
        y2 * LEAP_CYCLE_DAYS +
        (year - 1) * DAYS_IN_YEAR
    )

    mj = (month - 1) * 30
    dj = day - 1

    return 2375839.5 + yj + mj + dj


def _to_jd_equinox(an, mois, jour):
    day_of_adr = (30 * (mois - 1)) + (jour - 1)
    equinoxe = ephem.next_fall_equinox(str(an + YEAR_EPOCH))
    return trunc(dublin.to_jd(equinoxe.real) - 0.5) + 0.5 + day_of_adr


def from_jd(jd, method=None):
    '''Calculate date in the French Revolutionary
    calendar from Julian day.  The five or six
    "sansculottides" are considered a thirteenth
    month in the results of this function.'''
    method = method or 'equinox'

    if method == 'equinox':
        return _from_jd_equinox(jd)

    else:
        return _from_jd_schematic(jd, method)


def _from_jd_schematic(jd, method):
    if jd < EPOCH:
        raise ValueError("Can't convert days before the French Revolution")

    J = trunc(jd) + 0.5 - EPOCH

    # set p and r in Hatcher algorithm
    if method == 4:
        # these are ignored
        intercal_cycle_yrs = leap_suppression_yrs = 0
        intercal_cycle_days, leap_suppression_days = None, None

    elif method == 100:
        intercal_cycle_yrs = 400
        intercal_cycle_days = 146097  # 97 + 365 * 100
        leap_suppression_yrs = 100
        leap_suppression_days = 36524  # leap_cycle_days * 25 - 1

    elif method == 128:
        intercal_cycle_yrs = leap_suppression_yrs = 128
        intercal_cycle_days = 46751  # 31 + 128 * 365
        leap_suppression_days = 46751  # 32 * 1461 - 1

    else:
        raise ValueError("Unknown leap year method. Try: 4, 100, 128")

    if intercal_cycle_days:
        y0 = trunc(J / intercal_cycle_days)
        J = J - y0 * intercal_cycle_days
    else:
        y0 = 0

    if leap_suppression_days:
        y1 = trunc(J / leap_suppression_days)
        J = J - y1 * leap_suppression_days
    else:
        y1 = 0

    y2 = trunc(J / LEAP_CYCLE_DAYS)
    J = J - y2 * LEAP_CYCLE_DAYS

    y3 = trunc(J / DAYS_IN_YEAR)
    J = J - y3 * DAYS_IN_YEAR

    year = (
        y0 * intercal_cycle_yrs
        + y1 * leap_suppression_yrs
        + y2 * LEAP_CYCLE_YEARS + y3
    )

    month = trunc(J / 30)

    day = int(J - month * 30)

    return year + 1, month + 1, day + 1


def _from_jd_equinox(jd):
    '''Calculate the FR day using the equinox as day 1'''
    jd = trunc(jd) + 0.5
    equinoxe = premier_da_la_annee(jd)

    an = gregorian.from_jd(equinoxe)[0] - YEAR_EPOCH
    mois = trunc((jd - equinoxe) / 30) + 1
    jour = int((jd - equinoxe) % 30) + 1

    return (an, mois, jour)


def decade(jour):
    return trunc(jour / 10) + 1


def day_name(month, day):
    return french_republican_days[month][day - 1]


def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))


def to_gregorian(an, mois, jour):
    return gregorian.from_jd(to_jd(an, mois, jour))


def format(an, mois, jour):
    return "{0} {1} {2}".format(jour, MOIS[mois - 1], an)
