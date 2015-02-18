# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from math import floor, trunc
from itertools import chain
from .data import babylonian_data as data
from . import dublin, julian, gregorian
from .utils import amod, jwday, monthcalendarhelper
from pkg_resources import resource_stream
from csv import DictReader
import ephem
import codecs

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
    Dates in Terms of the Julian Calendar" into a dict.
    At the risk of being somewhat tortured in the conversions,
    the data is being generally preserved in the format they presented
    '''
    global PARKER_DUBBERSTEIN

    # Each row of P-D represents a babylonian year, which usually starts around
    # the Vernal Equinox
    if len(PARKER_DUBBERSTEIN) == 0:
        # header row:
        # ruler,regnalyear,astroyear,1,2,3,4,5,6,7,8,9,10,11,12,13,14
        # 12,13,14 will generally be in the next JYear
        with resource_stream('convertdate', 'data/parker-dubberstein.csv') as f:
            stringreader = codecs.getreader('ascii')
            reader = DictReader(stringreader(f))
            for row in reader:
                new = dict()
                year = int(row['jyear'])
                new['ruler'] = row['ruler']
                new['regnalyear'] = row['regnalyear']
                new['months'] = {}

                for monthid in [str(x) for x in range(1, 14)]:
                    if row.get(monthid):
                        jmonth, jday = row.get(monthid).split('/')
                        jmonth, jday = int(jmonth), int(jday)

                        # Have we swung over into the next year?
                        if jmonth < int(monthid):
                            jyear = year + 1
                        else:
                            jyear = year

                        new['months'][int(monthid)] = julian.to_jd(jyear, jmonth, jday)

                PARKER_DUBBERSTEIN[year] = new

    return PARKER_DUBBERSTEIN


def observer(date=None):
    '''Create a new ephem.Observer object for Babylon as the given date'''
    BABYLON = ephem.Observer()
    # OMFG I can't believe ephem uses d:mm:ss, wtf
    BABYLON.lat = '32:32:11'
    BABYLON.lon = '44:25:15'
    BABYLON.elevation = 32.536389

    if date:
        BABYLON.date = date

    return BABYLON


def _agyear(julianyear):
    '''Convert to AG (Seleucid) Epoch'''
    return julianyear - data.SELEUCID_EPOCH


def metonic_number(julianyear):
    '''The current year in the 19-year cycle. 20-22 are returned once per 687 years as leap-year correctives'''
    # Input should be the JY of the first day of the Babylonian year in question
    # Determine which 687-year cycle we're in

    # Year in the Seleucid era
    ag_year = _agyear(julianyear)

    return ag_metonic_number(ag_year)


def ag_metonic_number(ag_year):
    '''Returns the metonic number of the given year (AG)'''
    # The special years, outside of the cycle
    if ag_year > 0 and ag_year % 687 in [0, 685, 686]:
        return 21 - 687 + amod(ag_year, 687)

    base_year = _687_base_year(ag_year)

    # For most years, cycle runes 0-18, starts in base_year
    return (ag_year - base_year) % 19


def _687_base_year(ag_year):
    '''Year that the currrent cycle began: 1, 688, 1375, 2062'''
    return 1 + trunc((ag_year - 1) / 687) * 687


def _cycle_length(julianyear):
    '''Length of the "metonic" cycle of the given year. Usually 19, once every 687 years it's 22'''
    ag_year = _agyear(julianyear)

    # cycleyear will be in [0, 686]
    cycleyear = ag_year - _687_base_year(ag_year)

    # The 687-year super-cycle is 35 metonic cycles and one 22-year leap cycle. (19 * 35 + 22 = 687)
    # Integer division checks current sub-cycle of the super-cycle
    # 35 or 36 mean that we're in the last 22 years of the 687-year super-cycle
    if trunc(cycleyear / 19) >= 35:
        return 22

    return 19


def metonic_start(julianyear):
    '''The julian year that the metonic cycle of input began'''
    return julianyear - metonic_number(julianyear)


def intercalate(julianyear, plain=None, era=None):
    '''For a Julian year, use the intercalation pattern to return a dict of the months'''
    era = era or 'julian'
    if era.lower() == 'ag':
        return ag_intercalate(julianyear, plain=plain)

    number = metonic_number(julianyear)
    start = metonic_start(julianyear)
    return intercalation(number, start, plain)


def ag_intercalate(agyear, plain=None):
    '''For a Julian year, use the intercalation pattern to return a dict of the months'''
    number = ag_metonic_number(agyear)
    start = agyear - number
    return intercalation(number, start, plain)


def intercalation(mnumber, mstart=0, plain=None):
    '''A list of months for a given year (number) in a particular metonic cycle (start).
    Defaults to the standard intercalation'''

    if mstart < -633:
        raise IndexError("Input year out of range. The Babylonian calendar doesn't go that far back")

    pattern = data.intercalations.get(mstart, data.standard_intercalation)
    patternkey = pattern.get(mnumber)

    return intercalation_pattern(patternkey, plain)


def intercalation_pattern(key, plain=None):
    '''Return the list of months for a given intercalation type (U or A)'''
    if plain:
        base_list = data.ASCII_MONTHS
    else:
        base_list = data.MONTHS

    month, index = data.INTERCALARIES.get(key, (None, None))

    if month:
        months = base_list[:index] + [month] + base_list[index:]
    else:
        months = base_list

    return dict(list(zip(list(range(1, len(months) + 1)), months)))


def iterate_metonic_months(julianyear, plain=None):
    start = metonic_start(julianyear)
    c = _cycle_length(julianyear)
    years = range(start, start + c)
    return chain(*[list(intercalate(y, plain).values()) for y in years])


def month_count_to_cycle_year(count):
    """Given that we're <count> months into a metonic cycle, return the cycle-year [0, 21]"""
    if count > 272:
        raise ValueError("Month count too high")

    cumulative = 0
    for (year, months) in zip(range(0, 22), data.YEAR_LENGTH_LIST):
        cumulative = cumulative + months
        if count <= cumulative:
            return year


def _number_months(metonic_year):
    '''Number of months in the metonic year in the standard system'''
    if metonic_year in data.standard_intercalation:
        return 13
    else:
        return 12


def _valid_regnal(julianyear):
    if julianyear < -625 or julianyear > -145:
        return False
    return True


def regnalyear(julianyear):
    '''Determine regnal year based on a Julian year, -200 == 200 BC'''

    if _valid_regnal(julianyear):
        pass
    else:
        return (False, False)

    if julianyear in list(data.rulers.keys()):
        rulername = data.rulers[julianyear]
        ryear = 1
    else:
        key = max([r for r in data.rulers if r <= julianyear])
        ryear = julianyear - key + 1
        rulername = data.rulers[key]

    # Doesn't follow the rules, this guy.
    if rulername == 'Nabopolassar':
        ryear = ryear - 1

    if rulername == 'Alexander the Great':
        ryear = ryear + 6

    if rulername == 'Philip III Arrhidaeus':
        ryear = ryear + 1

    if rulername == 'Alexander IV Aegus':
        ryear = ryear + 1

    return (ryear, rulername)


def _regnal_epoch(ruler):
    '''Return the year that a ruler's epoch began'''

    if ruler.lower() in data.rulers_alt_names:
        ruler = data.rulers_alt_names[ruler.lower()]

    invert = dict((v, k) for k, v in list(data.rulers.items()))
    epoch = invert[ruler] - 1

    # Doesn't follow the rules, these guys
    if ruler == 'Nabopolassar':
        return epoch + 1

    if ruler == 'Alexander the Great':
        return epoch - 6

    if ruler == 'Philip III Arrhidaeus':
        return epoch - 1

    if ruler == 'Alexander IV Aegus':
        return epoch - 1

    return epoch


def _set_epoch(era=None):
    era = era or ''
    era = era.lower()

    if era == 'arsacid':
        return data.ARSACID_EPOCH
    elif era == 'nabonassar':
        return data.NABONASSAR_EPOCH
    elif era == 'nabopolassar':
        return data.NABOPOLASSAR_EPOCH
    else:
        return data.SELEUCID_EPOCH


def _numeral_month(year, month, era=None):
    '''Return the numeral of a Babylonian month. Month is either a digit or a string (babylonian month name)'''

    era = era or 'julian'

    if era.lower() not in ('julian', 'ag'):
        raise ValueError("Epoch must be 'julian' or 'ag' (alexanderian)")

    # easy cases
    if type(month) == float:
        month = int(month)

    months = intercalate(year, era=era)

    if type(month) == int:
        if month <= len(months):
            return month
        else:
            raise ValueError("Invalid month: {}. Wanted value <= {}. year: {}, era: {}".format(month, len(months), year, era))

    # Flip it around to get the month
    inverted = dict((v, k) for k, v in list(months.items()))

    try:
        month = inverted[month]
    except KeyError:

        months = ag_intercalate(year, era=era, plain=1)
        inverted = dict((v, k) for k, v in list(months.items()))

        month = inverted[month]
    except Exception as e:
        raise e

    return month


def from_jd(cjdn, era=None, plain=None):
    '''Calculate Babylonian date from Julian Day Count'''

    era = era or 'AG'

    if era.lower() == 'seleucid':
        era = 'AG'

    if cjdn > data.JDC_START_OF_ANALEPTIC:
        return _from_jd_analeptic(cjdn, era, plain)

    if cjdn < data.JDC_START_OF_REGNAL:
        raise IndexError('Date is too early for the Babylonian calendar')

    jyear = julian.from_jd(cjdn)[0]

    parkerdub = load_parker_dubberstein()

    # There's no row for the very last year in P-D's table
    if jyear == 46:
        jyear = jyear - 1

    pd = parkerdub[jyear]

    # Hop back to the previous row
    if cjdn < min(pd['months'].values()):
        jyear = jyear - 1
        pd = parkerdub[jyear]

    # The JDC of the months' first days => BMonth number (1..13)
    inverted = dict((v, k) for k, v in list(pd['months'].items()))

    # Start of the current month is highest JD not over input JDC
    start_of_month = max(mj for mj in list(inverted.keys()) if mj <= cjdn)

    # index of current month
    bmonth = inverted[start_of_month]

    # Get month name, taking into account intercalary months
    month_name = intercalate(jyear, plain).get(bmonth)

    # day of the month
    bday = cjdn - start_of_month + 1

    if era == 'regnal':
        by, era = regnalyear(jyear)
    else:
        by = jyear - _set_epoch(era)

    return (by, month_name, int(bday), era)


def to_jd(year, month, day, era=None, ruler=None):
    '''Convert Babylonian date to Julian Day Count'''
    if day < 1 or (type(month) in [int, float] and month < 1):
        raise ValueError("Month and day must be at least 1")

    era = era or ''

    if era.lower() not in ('arsacid', 'seleucid', 'ag', 'regnal') or era.lower == 'ag':
        era = 'AG'

    if era == 'regnal':
        if not ruler:
            raise ValueError("Missing argument for 'ruler'")
        epoch = _regnal_epoch(ruler)

    else:
        epoch = _set_epoch(era)

    if era.lower() in ('ag', 'seleucid') and year > 356:
        return _to_jd_analeptic(year, month, day, era=era)

    jyear = year + epoch

    # Find the row in parker-dubberstein's table that matches
    # our julian year and month.
    parkerdub = load_parker_dubberstein()

    month = _numeral_month(jyear, month, era='julian')

    try:
        pdentry = parkerdub[jyear]['months'][month]
    except KeyError:
        return _to_jd_analeptic(year, month, day, era=era)

    return pdentry + day - 1


def _to_jd_analeptic(year, month, day, era):
    if era == 'regnal':
        raise ValueError('Regnal era not valid for this date')

    if era.lower() not in ('arsacid', 'nabonassar', 'seleucid'):
        era = 'seleucid'

    month = _numeral_month(year, month, era='ag')

    epoch = _set_epoch(era)
    jyear = year + epoch

    # cycle number
    m = metonic_number(jyear)

    metonicstart = jyear - m

    moon = _nvnm_after_nve(dublin.from_julian(metonicstart, 1, 1))

    # Number of months we're into the current cycle
    months = month + sum(data.YEAR_LENGTH_LIST[0:m])

    for _ in range(1, months):
        moon = ephem.next_new_moon(moon)

    vnm = _moon_visibility(moon)

    outdc = floor(vnm + day) - 0.5

    return dublin.to_jd(outdc)


def to_julian(year, month, day, era=None, ruler=None):
    return julian.from_jd(to_jd(year, month, day, era, ruler))


def to_gregorian(year, month, day, era=None, ruler=None):
    return gregorian.from_jd(to_jd(year, month, day, era=era, ruler=ruler))


def from_julian(y, m, d, era=None, plain=None):
    return from_jd(julian.to_jd(y, m, d), era, plain=plain)


def from_gregorian(y, m, d, era=None, plain=None):
    return from_jd(gregorian.to_jd(y, m, d), era, plain=plain)


def _moon_visibility(newmoon):
    '''given a new moon (ephem.Date or dublin.dc), when is it visible'''
    babylon = observer()
    babylon.date = babylon.next_setting(SUN, start=newmoon)

    MOON.compute(babylon)

    if MOON.alt < 0:
        # Moon is down when the sun goes down.
        # Does it rise before morning?
        if babylon.next_rising(MOON) < babylon.next_rising(SUN):
            pass
        else:
            babylon.date = babylon.next_setting(SUN)

    # In Bab reckoning, the day started at sundown
    # For record-keeping, we use midnight
    # trunc sets up back to noon,
    # adding 0.5 takes us to the following midnight (day count = x.5)
    return ephem.Date(trunc(babylon.date) + 0.5)


def previous_visible_nm(dc):
    '''The previous time the new moon was visible in Babylon'''
    pnm = ephem.previous_new_moon(dc)
    visible = _moon_visibility(pnm)

    # Extra work to ensure that we're really before the input DC
    if visible > dc:
        visible = _moon_visibility(ephem.previous_new_moon(pnm))

    return visible


def next_visible_nm(dc):
    '''The next time the new moon will be visible in Babylon'''
    nnm = ephem.next_new_moon(dc)
    visible = _moon_visibility(nnm)

    # One bad possibility:
    # dc falls between NM and VNM:
    # ---NM---dc---VNM---
    # If so, we're actually a month later than the right answer
    if visible - dc > 28.5:
        # Check if dc is beform the end of the previous month
        pnm = ephem.previous_new_moon(dc)
        pnm_visible = _moon_visibility(pnm)
        if dc <= pnm_visible:
            visible = pnm_visible

    return visible


def _nvnm_after_pve(dc):
    '''Next visible new moon after the previous vernal equinox'''
    prev_equinox = ephem.previous_vernal_equinox(dc)
    return next_visible_nm(prev_equinox)


def _nvnm_after_nve(ephemdate):
    '''Next visible new moon after the next vernal equinox'''
    next_equinox = ephem.next_vernal_equinox(ephemdate)
    return next_visible_nm(next_equinox)


def moons_between_dates(start, end):
    '''Number of moons observed in Babylon between 2 ephem.Dates'''
    count = -1

    while start < end:
        start = ephem.next_new_moon(start)
        count += 1

    return count


def _correct_handoff(dublin_monthstart):
    '''Correct the handoff between Parker-Dubberstein records and the proleptic calendar'''
    if dublin_monthstart < dublin.from_julian(46, 3, 1):
        return ephem.Date((46, 2, 26))
    else:
        return dublin_monthstart


def _from_jd_analeptic(jdc, era=None, plain=None):
    '''Given a Julian Day Count, calculate the Babylonian date analeptically, with choice of eras'''
    # Make sure we're at midnight
    jdc = int(jdc) + 0.5
    era = era or 'AG'

    # Calcuate the dublin day count, used in ephem
    dublincount = dublin.from_jd(jdc)

    # Start of the current month
    monthstart = previous_visible_nm(dublincount)
    monthstart = _correct_handoff(monthstart)

    # We're now at the start of the metonic cycle that contains
    # the year we're in. Call this M0
    julianyear, _, _ = julian.from_gregorian(*monthstart.triple())
    metonicstart = metonic_start(julianyear)

    # This is a list of all the months in this cycle
    month_iter = iterate_metonic_months(metonicstart, plain)
    past_months = []

    # Start of the BY that begins in JY M0
    moon = _nvnm_after_nve((metonicstart, 1, 1))

    # Loop through NMs until we arrive at close to monthstart
    # 3 is a fudge factor to make sure we don't fall between NM and visibility
    # We move months from the active list to a past list
    while moon + 3 < monthstart:
        moon = ephem.next_new_moon(moon)
        past_months.append(next(month_iter))

    # month name is next month in queue
    month_name = next(month_iter)

    # set year with month name and epoch
    cycleyear = month_count_to_cycle_year(len(past_months) + 1)

    year = metonicstart + cycleyear
    epoch = _set_epoch(era)

    day_count = int(dublincount - monthstart) + 1

    return year - epoch, month_name, day_count, era


def day_duration(jdc):
    '''The start and end times of the Babylonian day that overlaps with noon on the day of the input.
    For best results, pass a Julian Day Count with a decimal of .5 (e.g. 1737937.5)
    '''
    ddc = dublin.from_jd(jdc)
    babylon = observer(ddc)

    start = babylon.previous_setting(SUN)
    end = babylon.next_setting(SUN)

    return dublin.to_datetime(start), dublin.to_datetime(end)


def month_length(jd):
    '''Get the length (in days) of the Babylonian month that jd falls in'''
    start = previous_visible_nm(dublin.from_jd(jd + 0.5))
    end = next_visible_nm(dublin.from_jd(jd + 0.5))
    return int(end - start)


def monthcalendar(agyear, month):
    '''Produce a list of lists that reflects a calendar for the given year (AG) and month'''
    jd = to_jd(agyear, month, 1)
    start_weekday = jwday(jd)

    monthlen = month_length(jd)

    return monthcalendarhelper(start_weekday, monthlen)

