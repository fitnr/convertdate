# -*- coding: utf-8 -*-
import babylonian_data as data
import julian

# INTERCALARY = u"Makaruša"

# todo:
# jd_to_seleucid_era
# jd_to_arasid era
#
def intercalate(julianyear):
    '''For a Julian year, use the intercalation pattern to return a dict of the months'''
    # Add 1 because cycle runs 1-19 in Parker & Dubberstein
    metonic_year = 1 + ((julianyear - 14) % 19)
    # 1 + (year mod 19) == 15 is year 1 of the metonic cycle.
    metonic_start = julianyear - metonic_year + 1

    intercalation_pattern = data.intercalations.get(metonic_start, data.standard_intercalation)
    patternkey = intercalation_pattern.get(metonic_year)

    month, index = data.INTERCALARIES.get(patternkey, ([], len(data.MONTHS)))
    months = data.MONTHS[:index] + month + data.MONTHS[index:]

    return dict(zip(range(1, len(months) + 1), months))

def regnalyear(by):
    '''Determine regnal year'''
    if (by < -436):
        return

    regnalyear = by - key + 1
    rulername = rulers[key]
    key = max([r for r in data.rulers if r <= by])

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


def get_start_jd_of_month(y, m):
    return [key for key, val in data.lunations.items() if val[0] == y and val[1] == m].pop()

def month_length(by, bm):
    j = get_start_jd_of_month(by, bm)

    possible_keys = [x for x in data.lunations if x < j + 31 and x > j]
    next_month = possible_keys.pop()

    return next_month - j + 1


def from_jd(cjdn):
    '''Calculate Babylonian date from Julian Day Count'''
    if (cjdn < 1492871 or cjdn > 1748872):
        raise IndexError

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


def to_jd(year, month, day):
    key = get_start_jd_of_month(year, month)
    return key + day - 1



