import astro
from julian import Julianday


EPOCH = 1948320.5
WEEKDAYS = ("Yekshanbeh", "Doshanbeh",
            "Seshhanbeh", "Chaharshanbeh",
            "Panjshanbeh", "Jomeh", "Shanbeh")


def leap(year):
    '''LEAP  --  Is a given year a leap year in the Persian calendar ?'''
    if year > 0:
        y = 474
    else:
        y = 473

    return ((((((year - y % 2820) + 474) + 38) * 682) % 2816) < 682)
    # return ((((((year - ((year > 0) ? 474 : 473)) % 2820) + 474) + 38) *
    # 682) % 2816) < 682;


def to_jd(year, month, day):
    '''TO_JD  --  Determine Julian day from Persian date'''

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

    return Julianday(day +
                     m +
                     astro.floor(((epyear * 682) - 110) / 2816) +
                    (epyear - 1) * 365 +
                     astro.floor(epbase / 2820) * 1029983 +
                    (EPOCH - 1))
