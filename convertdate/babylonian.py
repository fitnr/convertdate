# -*- coding: utf-8 -*-
from __future__ import division
from itertools import chain
from .data import babylonian_data as data
from . import dublin, julian, gregorian
from pkg_resources import resource_stream
from csv import DictReader
import ephem

MOON = ephem.Moon()
SUN = ephem.Sun()

# At JDC 1000.0, it was 1000.125 in Babylon
# AST = Babylon's time zone
AST_ADJUSTMENT = 0.125

# todo:
# from_jd (seleucid, arascid, regnal year)

PARKER_DUBBERSTEIN = dict()

# Example row:
# -604: {
#   'ruler': 'NABOPOLASSAR',
#   'year': -604,
#   'regnalyear': '21',
#   'months': {
#       1: 1500913.5,
#       2: 1500942.5,
#       3: 1500972.5,
#       4: 1501001.5,
#       5: 1501031.5,
#       6: 1501061.5,
#       7: 1501090.5,
#       8: 1501120.5,
#       9: 1501149.5,
#       10: 1500814.5,
#       11: 1500843.5,
#       12: 1500873.5,
#   },
# }



def load_parker_dubberstein():
    '''Read the P-D "Table for the Restatement of Babylonian
    Dates in Terms of the Julian Calendar" into a dict'''

    global PARKER_DUBBERSTEIN

    # header row:
    # ruler,regnalyear,astroyear,1,2,3,4,5,6,7,8,9,10,11,12,13,14
    with resource_stream('convertdate', 'data/parker-dubberstein.csv') as f:
        reader = DictReader(f)
        for row in reader:
            new = dict()
            year = int(row['jyear'])
            new['ruler'] = row['ruler']
            new['regnalyear'] = row['regnalyear']
            new['months'] = {}

            for monthid in [str(x) for x in range(1, 15)]:
                if row.get(monthid):
                    month, day = row.get(monthid).split('/')
                    new['months'][int(monthid)] = julian.to_jd(year, int(month), int(day))

            PARKER_DUBBERSTEIN[year] = new


def observer(date):
    BABYLON = ephem.Observer()
    # OMFG I can't believe ephem uses d:mm:ss, wtf
    BABYLON.lat = '32:32:11'
    BABYLON.lon = '44:25:15'
    BABYLON.elevation = 32.536389

    if date:
        BABYLON.date = date

    return BABYLON


def metonic_number(julianyear):
    '''The start year of the current metonic cycle and the current year (1-19) in the cycle'''
    # Input should be the JY of the first day of the Babylonian year in question
    # Add 1 because cycle runs 1-19 in Parker & Dubberstein
    if julianyear == 0:
        raise IndexError("There was no year zero")

    if julianyear > 0:
        julianyear = julianyear - 1

    return 1 + ((julianyear - 13) % 19)


def metonic_start(julianyear):
    '''The julian year that the metonic cycle of input began'''
    if julianyear == 0:
        raise IndexError("There was no year zero")

    m = metonic_number(julianyear)

    if julianyear > 0:
        julianyear = julianyear - 1

    return julianyear - m + 1


def intercalate(julianyear):
    '''For a Julian year, use the intercalation pattern to return a dict of the months'''
    number = metonic_number(julianyear)
    start = metonic_start(julianyear)
    return intercalation(number, start)


def intercalation(mnumber, mstart=0):
    '''A list of months for a given year (number) in a a particular metonic cycle (start).
    Defaults to the standard intercalation'''

    if mstart < -747:
        raise IndexError("Input year out of range. The Babylonian calendar doesn't go that far back")

    pattern = data.intercalations.get(mstart, data.standard_intercalation)
    patternkey = pattern.get(mnumber)

    return intercalation_pattern(patternkey)


def intercalation_pattern(key):
    month, index = data.INTERCALARIES.get(key, (None, None))

    if month:
        months = data.MONTHS[:index] + [month] + data.MONTHS[index:]
    else:
        months = data.MONTHS

    return dict(zip(range(1, len(months) + 1), months))


def standard_metonic_month_list():
    return list(chain(*[intercalation(y).values() for y in range(1, 20)]))


def _number_months(metonic_year):
    '''Number of months in the metonic year in the standard system'''
    if metonic_year in data.standard_intercalation:
        return 13
    else:
        return 12


def _valid_regnal(julianyear):
    if julianyear < -749 or julianyear > -146:
        return False
    return True


def regnalyear(julianyear):
    '''Determine regnal year based on a Julian year, -200 == 200 BC'''
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


def _month_name(monthindex):
    '''Given the number of the month in the metonic cycle of 235, return the name of the month'''

    # Get a number between 0 and 235
    monthindex = monthindex % 235

    if monthindex == 0:
        monthindex = 235

    # Use to 0 index
    return standard_metonic_month_list().pop(monthindex - 1)


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


def from_julian(y, m, d, era=None):
    return from_jd(julian.to_jd(y, m, d), era)


def from_gregorian(y, m, d, era=None):
    return from_jd(gregorian.to_jd(y, m, d), era)


def next_visible_nm(dc):
    nnm = ephem.next_new_moon(dc)
    babylon = observer(nnm)

    SUN.compute(babylon)

    while SUN.alt > 0:
        next_moonrise = babylon.next_rising(MOON, start=nnm)
        SUN.compute(babylon)

    return next_moonrise

def _fromjd_proleptic(jdc, epoch):
    '''Given a Julian Day Count, calculate the Babylonian date proleptically, with choice of eras'''
    # Calcuate the dublin day count, used in ephem
    # We're going to return the date for noon
    jdc = int(jdc) + 0.5

    dublincount = dublin.from_jd(jdc)

    # Are we before or after the VE of this Gregorian year?
    # If the next VE is in the current year, the year will be the previous one... probably
    # Get start date of current metonic cycle
    julian_date = julian.from_jd(jdc)
    mstart = metonic_start(julian_date[0])
    metonic_equinox = ephem.previous_vernal_equinox('/'.join([str(mstart), '7', '1']))

    # Only the VE in the metonic base year matters
    # Loop through the new moons since the metonic base
    new_moon = moon = next_visible_nm(metonic_equinox)
    mooncount = 0

    # count forward until we're in the current month
    while new_moon < dublincount:
        mooncount = 1 + mooncount

        moon = new_moon

        new_moon = next_visible_nm(moon)

    month_name = _month_name(mooncount)

    day_count = int(dublincount - new_moon)

    return days, month_name, epoch + julian_date[0]

