from utils import ceil, floor


EPOCH = 1948320.5
WEEKDAYS = ("Yekshanbeh", "Doshanbeh",
            "Seshhanbeh", "Chaharshanbeh",
            "Panjshanbeh", "Jomeh", "Shanbeh")


def leap(year):
    '''Is a given year a leap year in the Persian calendar ?'''
    if year > 0:
        y = 474
    else:
        y = 473

    return ((((((year - y % 2820) + 474) + 38) * 682) % 2816) < 682)


def to_jd(year, month, day):
    '''Determine Julian day from Persian date'''

    if year >= 0:
        y = 474
    else:
        y = 473
    epbase = year - y
    epyear = 474 + (epbase % 2820)

    if month <= 7:
        m = (month - 1) * 31
    else:
        m = (month - 1) * 30 + 6

    return day + m + floor(((epyear * 682) - 110) / 2816) + (epyear - 1) * 365 + floor(epbase / 2820) * 1029983 + (EPOCH - 1)


def from_jd(jd):
    '''Calculate Persian date from Julian day'''
    jd = floor(jd) + 0.5

    depoch = jd - to_jd(475, 1, 1)
    cycle = floor(depoch / 1029983)
    cyear = (depoch % 1029983)

    if cyear == 1029982:
        ycycle = 2820
    else:
        aux1 = floor(cyear / 366)
        aux2 = cyear % 366
        ycycle = floor(((2134 * aux1) + (2816 * aux2) + 2815) / 1028522) + aux1 + 1

    year = ycycle + (2820 * cycle) + 474

    if (year <= 0):
        year -= 1

    yday = (jd - to_jd(year, 1, 1)) + 1

    if yday <= 186:
        month = ceil(yday / 31)
    else:
        month = ceil((yday - 6) / 30)

    day = int(jd - to_jd(year, month, 1)) + 1

    return (year, month, day)
