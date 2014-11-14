# -*- coding: utf-8 -*-
import time
from math import trunc
import calendar
from . import hebrew


# time tuple/list index
YEAR = 0
MONTH = 1
DAY = 2
WEEKDAY = 6

# weekdays
MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6

# months
JAN = 1
FEB = 2
MAR = 3
APR = 4
MAY = 5
JUN = 6
JUL = 7
AUG = 8
SEP = 9
OCT = 10
NOV = 11
DEC = 12

# Hebrew months
NISAN = 1
IYYAR = 2
SIVAN = 3
TAMMUZ = 4
AV = 5
ELUL = 6
TISHRI = 7
HESHVAN = 8
KISLEV = 9
TEVETH = 10
SHEVAT = 11
ADAR = 12
VEADAR = 13


def adjust_date(timelist):
    '''after a date calculation, this method will coerce the list members to ensure
       that they are within the correct bounds. That is, a date of Oct 32
       becomes Nov 1, etc'''
    tm = (timelist[YEAR], timelist[
        MONTH], timelist[DAY], 0, 0, 0, 0, 0, -1)
    e = time.mktime(tm)
    tm = time.localtime(e)
    timelist[MONTH] = tm[MONTH]
    timelist[DAY] = tm[DAY]

    return timelist


def nth_day_of_month(n, weekday, month, year):
    '''Return (year, month, day) tuple that represents nth weekday of month in year. If n==0, returns last weekday of month'''
    if not (0 <= n <= 5):
        raise IndexError("Nth day of month must be 0-5. Received: {}".format(n))

    if not (0 <= weekday <= 6):
        raise IndexError("Weekday must be 0-6")

    firstday, daysinmonth = calendar.monthrange(year, month)

    # Get first WEEKDAY of month
    first_weekday_of_kind = 1 + (weekday - firstday) % 7

    if n == 0:
        # find last weekday of kind, which is 5 if these conditions are met, else 4
        if first_weekday_of_kind in [1, 2, 3] and first_weekday_of_kind + 28 < daysinmonth:
            n = 5
        else:
            n = 4

    day = first_weekday_of_kind + ((n - 1) * 7)

    if day > daysinmonth:
        raise IndexError("No {}th day of month {}".format(n, month))

    return (year, month, day)


def new_years(year):
    '''Jan 1st'''
    return (year, JAN, 1)


def martin_luther_king_day(year):
    '''third monday in January'''
    return nth_day_of_month(3, MON, JAN, year)


def lincolns_birthday(year):
    '''Feb 12'''
    return (year, FEB, 12)


def valentines_day(year):
    '''feb 14th'''
    return (year, FEB, 14)


def washingtons_birthday(year):
    '''Feb 22'''
    return (year, FEB, 22)


def presidents_day(year):
    '''3rd Monday of Feb'''
    return nth_day_of_month(3, MON, FEB, year)


def pulaski_day(year):
    '''1st monday in March'''
    return nth_day_of_month(1, MON, MAR, year)


def easter(year):
    '''Calculate western easter'''
    # formula taken from http://aa.usno.navy.mil/faq/docs/easter.html
    c = trunc(year / 100)
    n = year - 19 * trunc(year / 19)

    k = trunc((c - 17) / 25)

    i = c - trunc(c / 4) - trunc((c - k) / 3) + (19 * n) + 15
    i = i - 30 * trunc(i / 30)
    i = i - trunc(i / 28) * (1 - trunc(i / 28) * trunc(29 / (i + 1)) * trunc((21 - n) / 11))

    j = year + trunc(year / 4) + i + 2 - c + trunc(c / 4)
    j = j - 7 * trunc(j / 7)

    l = i - j

    month = 3 + trunc((l + 40) / 44)
    day = l + 28 - 31 * trunc(month / 4)

    return year, int(month), int(day)


def may_day(year):
    return (year, MAY, 1)


def mothers_day(year):
    '''2nd Sunday in May'''
    return nth_day_of_month(2, SUN, MAY, year)


def memorial_day(year):
    '''last Monday in May'''
    return nth_day_of_month(0, MON, MAY, year)


def fathers_day(year):
    '''3rd Sunday in June'''
    return nth_day_of_month(3, SUN, JUN, year)


def flag_day(year):
    '''June 14th'''
    return (year, JUN, 14)


def indepedence_day(year, observed=None):
    '''July 4th'''
    day = 4

    if observed:
        if calendar.weekday(year, JUL, 4) == SAT:
            day = 3

        if calendar.weekday(year, JUL, 4) == SUN:
            day = 5

    return (year, JUL, day)


def labor_day(year):
    '''first Monday in Sep'''
    return nth_day_of_month(1, MON, SEP, year)


def columbus_day(year, country='usa'):
    '''in USA: 2nd Monday in Oct
       Elsewhere: Oct 12'''
    if country == 'usa':
        return nth_day_of_month(2, MON, OCT, year)
    else:
        return (year, OCT, 12)


def halloween(year):
    '''Oct 31'''
    return (year, OCT, 31)


def election_day(year):
    '''1st Tues in Nov'''
    return nth_day_of_month(1, TUE, NOV, year)


def veterans_day(year):
    '''Nov 11'''
    return (year, NOV, 11)


def rememberance_day(year):
    return veterans_day(year)


def armistice_day(year):
    return veterans_day(year)


def thanksgiving(year, country='usa'):
    '''USA: last Thurs. of November, Canada: 2nd Mon. of October'''
    if country == 'usa':
        if year in [1940, 1941]:
            return nth_day_of_month(3, THU, NOV, year)
        elif year == 1939:
            return nth_day_of_month(4, THU, NOV, year)
        else:
            return nth_day_of_month(0, THU, NOV, year)

    if country == 'canada':
        return nth_day_of_month(2, MON, OCT, year)


def christmas_eve(year):
    '''24th of December'''
    return (year, DEC, 24)


def christmas(year):
    '''25th of December'''
    return (year, DEC, 25)


def new_years_eve(year):
    '''Dec 31st'''
    return (year, DEC, 31)

# Jewish holidays begins the sunset before the first (secular) day of the holiday
# With the eve option set, the day of this sunset is returned
# without the option, the (secular) day is returned


def hanukkah(year, eve=False):
    year, month, day = hebrew.to_jd_gregorianyear(year, KISLEV, 25)
    if eve:
        day = day - 1
    return year, month, day


def rosh_hashanah(year, eve=False):
    year, month, day = hebrew.to_jd_gregorianyear(year, TISHRI, 1)
    if eve:
        day = day - 1
    return year, month, day


def yom_kippur(year, eve=False):
    year, month, day = hebrew.to_jd_gregorianyear(year, TISHRI, 10)
    if eve:
        day = day - 1

    return year, month, day


def passover(year, eve=False):
    year, month, day = hebrew.to_jd_gregorianyear(year, NISAN, 15)
    if eve:
        day = day - 1

    return year, month, day


class Holidays(object):

    def __init__(self, year=None):
        self.year = year or time.localtime().tm_year

    def set_year(self, year):
        self.year = year

    # the holidays...
    @property
    def christmas(self):
        return christmas(self.year)

    @property
    def christmas_eve(self):
        return christmas_eve(self.year)

    @property
    def thanksgiving(self, country='usa'):
        return thanksgiving(self.year, country)

    @property
    def new_years(self):
        return new_years(self.year)

    @property
    def new_years_eve(self):
        return new_years_eve(self.year)

    @property
    def indepedence_day(self, observed=None):
        return indepedence_day(self.year, observed)

    @property
    def flag_day(self):
        return flag_day(self.year)

    @property
    def election_day(self):
        return election_day(self.year)

    @property
    def presidents_day(self):
        return presidents_day(self.year)

    @property
    def washingtons_birthday(self):
        return washingtons_birthday(self.year)

    @property
    def lincolns_birthday(self):
        return lincolns_birthday(self.year)

    @property
    def memorial_day(self):
        return memorial_day(self.year)

    @property
    def labor_day(self):
        return labor_day(self.year)

    @property
    def columbus_day(self, country='usa'):
        return columbus_day(self.year, country)

    @property
    def veterans_day(self):
        return veterans_day(self.year)

    @property
    def valentines_day(self):
        return valentines_day(self.year)

    @property
    def halloween(self):
        return halloween(self.year)

    @property
    def mothers_day(self):
        return mothers_day(self.year)

    def fathers_day(self):
        return fathers_day(self.year)

    @property
    def easter(self):
        return easter(self.year)

    @property
    def martin_luther_king_day(self):
        return martin_luther_king_day(self.year)

    @property
    def hanukkah(self, eve=None):
        return hanukkah(self.year, eve)

    @property
    def rosh_hashanah(self, eve=None):
        return rosh_hashanah(self.year, eve)

    @property
    def yom_kippur(self, eve=None):
        return yom_kippur(self.year, eve)

    @property
    def passover(self, eve=None):
        return passover(self.year, eve)


if __name__ == '__main__':
    holiday = Holidays(2014)
