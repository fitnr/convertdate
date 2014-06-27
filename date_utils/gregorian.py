from calendar_util import Julianday
from astro import floor


EPOCH = 1721425.5


def leap(year):
    return (year % 4 == 0 and not ((year % 100) == 0 and (year % 400) != 0))


def gregorian_to_jd(year, month, day):
    if month <= 2:
        leap_adj = 0
    elif leap(year):
        leap_adj = -1
    else:
        leap_adj = -2

    return Julianday(
      (EPOCH - 1) + (365 * (year - 1)) + floor((year - 1) / 4) +
      (-floor((year - 1) / 100)) + floor((year - 1) / 400) +
      floor((((367 * month) - 362) / 12) + leap_adj + day)
    )
