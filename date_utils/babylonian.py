# -*- coding: utf-8 -*-
from __future__ import division
import babylonian_data as data
from utils import floor
import julian
import ephem

DUBLIN_EPOCH = 2415020  # Julian Day Count for Dublin Count 0

BABYLON = ephem.Observer()
BABYLON.lat, BABYLON.lon, BABYLON.elevation = 32.536389, 44.420833, 35.18280792236328

MOON = ephem.Moon()
SUN = ephem.Sun()

# At JDC 1000.0, it was 1000.125 in Babylon
AST_ADJUSTMENT = 0.125

# todo:
# from_jd (seleucid, arascid, regnal year)


def _metonic_number(julianyear):
    '''The start year of the current metonic cycle and the current year (1-19) in the cycle'''
    # Input should be the JY of the first day of the Babylonian year in question
    # Add 1 because cycle runs 1-19 in Parker & Dubberstein
    return 1 + ((julianyear - 14) % 19)


def _metonic_start(julianyear):
    '''The julian year that the metonic cycle of input began'''
    return julianyear - _metonic_number(julianyear) + 1


def intercalate(julianyear):
    '''For a Julian year, use the intercalation pattern to return a dict of the months'''
    metonic_number = _metonic_number(julianyear)
    metonic_start = _metonic_start(julianyear)
    return data.intercalation(metonic_number, metonic_start)


def _number_months(metonic_year):
    '''Number of months in the metonic year in the standard system'''
    if metonic_year in data.standard_intercalation:
        return 13
    else:
        return 12


def _valid_regnal(julianyear):
    if julianyear < -748 or julianyear > -149:
        return False
    return True


def regnalyear(julianyear):
    '''Determine regnal year'''
    if not _valid_regnal(julianyear):
        return False

    key = max([r for r in data.rulers if r <= julianyear])

    ryear = julianyear - key + 1

    rulername = data.rulers[key]

    if rulername == 'Alexander the Great':
        ryear = ryear + 6

    if rulername == "Philip III Arrhidaeus":
        ryear = ryear + 1

    if rulername == 'Alexander IV Aegus':
        ryear = ryear + 1

    return (ryear, rulername)


def _set_epoch(era):
    if era == 'arascid':
        return -data.ARASCID_EPOCH
    elif era == 'nabonassar':
        return -data.NABONASSAR_EPOCH
    else:
        return -data.SELEUCID_EPOCH


def arsacid_year(by):
    if by > 64:
        return by - 64


def get_start_jd_of_month(y, m):
    return [key for key, val in data.lunations.items() if val[0] == y and val[1] == m].pop()


def month_length(by, bm):
    j = get_start_jd_of_month(by, bm)

    possible_keys = [x for x in data.lunations if x < j + 31 and x > j]
    next_month = possible_keys.pop()

    return next_month - j + 1


def from_jd(cjdn, era='seleucid'):
    '''Calculate Babylonian date from Julian Day Count'''
    if cjdn < 1492871:
        raise IndexError

    if era == 'regnal' and cjdn > 1670999.5:
        era = 'seleucid'

    epoch = _set_epoch(era)

    if cjdn > 1748872:
        return _fromjd_proleptic(cjdn, epoch)

    # pd is the period of the babylonian month cjdn is found in
    pd = [lu for lu in data.lunations.keys() if lu < cjdn and lu + 31 > cjdn].pop()
    by, bm = data.lunations[pd]

    # Day of the month
    bd = cjdn - pd + 1

    juliandate = julian.from_jd(cjdn)

    months = intercalate(juliandate[0])

    # document.calendar.bmonth.selectedIndex            = bm-1

    # compute and output the date in the babylonian lunar calendar
    # bln = 1498 + i
    # document.calendar.blunnum.value                   = bln
    # document.calendar.bmlength.value                  = bml

    return (bd, months[bm], by)


def to_jd(y, m, d):
    key = get_start_jd_of_month(y, m)
    return key + d - 1


def from_gregorian(y, m, d, era):
    return from_jd(julian.to_jd(y, m, d), era)


def _rising_babylon(dc, func, body):
    '''Given a date, body and function, give the next rising of that body after function occurs'''
    event = func(dc)
    return BABYLON.next_rising(body, start=event)


def _setting_babylon(dc, func, body):
    '''Given a date, body and function, give the next setting of that body after function occurs'''
    event = func(dc)
    return BABYLON.next_setting(body, start=event)


def _prev_new_rising_babylon(dublindc):
    '''Given a Dublin DC, give the previous nm rising in Babylon'''
    return _rising_babylon(dublindc, ephem.previous_new_moon, MOON)


def _next_new_rising_babylon(dublindc):
    '''Given a Dublin DC, give the previous nm rising in Babylon'''
    return _rising_babylon(dublindc, ephem.next_new_moon, MOON)


def _body_up(dc, observer, body):
    '''Checks if body is visible in the sky right now at observer'''
    observer.date = dc
    if observer.next_setting(body) < observer.next_rising(body):
        return True
    else:
        return False


def _babylon_daytime(dc):
    return _body_up(dc, BABYLON, SUN)


def _fromjd_proleptic(jdc, epoch):
    # calculate previous vernal equinox of jdc

    pass

