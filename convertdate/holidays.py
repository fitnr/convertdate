# -*- coding: utf-8 -*-
import time
from copy import copy
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
Nisan = 1
Iyyar = 2
Sivan = 3
Tammuz = 4
Av = 5
Elul = 6
Tishri = 7
Heshvan = 8
Kislev = 9
Teveth = 10
Shevat = 11
Adar = 12
Veadar = 13

HAVE_30_DAYS = (APR, JUN, SEP, NOV)
HAVE_31_DAYS = (JAN, MAR, MAY, JUL, AUG, OCT, DEC)

SECONDS_PER_DAY = 60 * 60 * 24


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
    '''Return the nth weekday of month in year'''
    # returns the day of the month 1..31
    if not year:
        raise IndexError

    firstday, daysinmonth = calendar.monthrange(year, month)

    # Get first WEEKDAY of month
    # firstday is MON, weekday is WED -- start with 3rd day of month
    # firstday is WED, weekday is MON --
    # firstday = weekday
    if firstday < weekday:
        date = weekday - firstday + 1  # 2 - 0 + 1
    elif firstday > weekday:
        date = 7 - (firstday - weekday) + 1
    else:
        date = 1

    if n == 1:
        return date

    # Get nth WEEKDAY of month. Subtract 1 because already have 1st
    date += (n - 1) * 7

    if month in HAVE_30_DAYS and date > 30:
        raise IndexError
    if month in HAVE_31_DAYS and date > 31:
        raise IndexError
    if month == FEB and date > 28:
        ignore, daysinfeb = calendar.monthrange(year, FEB)
        if date > daysinfeb:
            raise IndexError

    return date


class Holidays(object):

    def __init__(self, year=None, ymd=False):
        self.time_list = list(time.localtime())

        if year:
            self.set_year(year)

        if ymd:
            self.ymd = True

    def get_epoch(self):
        t = tuple(self.time_list)
        return time.mktime(t)

    def set_year(self, year):
        self.time_list[YEAR] = year

    def returnwrapper(self, tl):
        if self.ymd:
            return (tl[YEAR], tl[MONTH], tl[DAY])
        else:
            return tl

    @property
    def timelist(self):
        return self.time_list

    # the holidays...
    @property
    def christmas(self):
        '''25th of December'''
        tl = copy(self.timelist)
        tl[MONTH] = DEC
        tl[DAY] = 25
        return self.returnwrapper(tl)

    @property
    def christmas_eve(self):
        '''24th of December'''
        tl = copy(self.timelist)
        tl[MONTH] = DEC
        tl[DAY] = 24
        return self.returnwrapper(tl)

    @property
    def thanksgiving(self):
        '''4th Thursday of November'''
        tl = copy(self.timelist)
        tl[MONTH] = NOV
        tl[DAY] = nth_day_of_month(4, THU, NOV, tl[YEAR])
        return self.returnwrapper(tl)

    @property
    def new_years(self):
        '''Jan 1st'''
        tl = copy(self.timelist)

        tl[MONTH] = JAN
        tl[DAY] = 1

        return self.returnwrapper(tl)

    @property
    def new_years_eve(self):
        '''Dec 31st'''
        tl = copy(self.timelist)

        tl[MONTH] = DEC
        tl[DAY] = 31

        return self.returnwrapper(tl)

    @property
    def indepedence_day(self, observed=None):
        '''July 4th'''
        tl = copy(self.timelist)
        tl[MONTH] = JUL
        tl[DAY] = 4

        if observed:
            if tl[WEEKDAY] == SAT:
                tl[DAY] = 3

            if tl[WEEKDAY] == SUN:
                tl[DAY] = 5

        return self.returnwrapper(tl)

    @property
    def flag_day(self):
        '''June 14th'''
        tl = copy(self.timelist)
        tl[MONTH] = JUN
        tl[DAY] = 14
        return self.returnwrapper(tl)

    @property
    def election_day(self):
        '''1st Tues in Nov'''
        tl = copy(self.timelist)
        tl[MONTH] = NOV
        tl[DAY] = nth_day_of_month(1, TUE, NOV, tl[YEAR])
        return self.returnwrapper(tl)

    @property
    def presidents_day(self):
        '''3rd Monday of Feb'''
        tl = copy(self.timelist)
        tl[MONTH] = NOV
        tl[DAY] = nth_day_of_month(3, MON, FEB, tl[YEAR])
        return self.returnwrapper(tl)

    @property
    def washingtons_birthday(self):
        '''Feb 22'''
        tl = copy(self.timelist)
        tl[MONTH] = FEB
        tl[DAY] = 22
        return self.returnwrapper(tl)

    @property
    def lincolns_birthday(self):
        '''Feb 12'''
        tl = copy(self.timelist)
        tl[MONTH] = FEB
        tl[DAY] = 12
        return self.returnwrapper(tl)

    @property
    def memorial_day(self):
        '''last Monday in May'''
        tl = copy(self.timelist)
        tl[MONTH] = MAY
        # if May has 5 Mondays...
        try:
            tl[DAY] = nth_day_of_month(5, MON, MAY, tl[YEAR])
        except IndexError:
            # otherwise, May has only 4 Mondays
            tl[DAY] = nth_day_of_month(4, MON, MAY, tl[YEAR])
        return self.returnwrapper(tl)

    @property
    def labor_day(self):
        '''first Monday in Sep'''
        tl = copy(self.timelist)
        tl[MONTH] = SEP
        tl[DAY] = nth_day_of_month(1, MON, SEP, tl[YEAR])

        return self.returnwrapper(tl)

    @property
    def columbus_day(self, UnitedStates=1):
        '''in USA: 2nd Monday in Oct
           Elsewhere: Oct 12'''
        tl = copy(self.timelist)
        tl[MONTH] = OCT
        if UnitedStates:
            tl[DAY] = nth_day_of_month(2, MON, OCT, tl[YEAR])
        else:
            tl[DAY] = 12

        return self.returnwrapper(tl)

    @property
    def veterans_day(self):
        '''Nov 11'''
        tl = copy(self.timelist)
        tl[MONTH] = NOV
        tl[DAY] = 11
        return self.returnwrapper(tl)

    @property
    def valentines_day(self):
        '''feb 14th'''
        tl = copy(self.timelist)
        tl[MONTH] = FEB
        tl[DAY] = 14
        return self.returnwrapper(tl)

    @property
    def halloween(self):
        '''Oct 31'''
        tl = copy(self.timelist)
        tl[MONTH] = OCT
        tl[DAY] = 31
        return self.returnwrapper(tl)

    @property
    def mothers_day(self):
        '''2nd Sunday in May'''
        tl = copy(self.timelist)
        tl[MONTH] = MAY
        tl[DAY] = nth_day_of_month(2, SUN, MAY, tl[YEAR])
        return self.returnwrapper(tl)

    @property
    def fathers_day(self):
        '''3rd Sunday in June'''
        tl = copy(self.timelist)
        tl[MONTH] = JUN
        tl[DAY] = nth_day_of_month(3, SUN, JUN, tl[YEAR])
        return self.returnwrapper(tl)

    @property
    def easter(self):
        tl = copy(self.timelist)
        y = tl[YEAR]

        # formula taken from http://aa.usno.navy.mil/faq/docs/easter.html
        c = (y / 100)
        n = y - 19 * (y / 19)
        k = (c - 17) / 25
        i = c - c / 4 - (c - k) / 3 + 19 * n + 15
        i = i - 30 * (i / 30)
        i = i - (i / 28) * (1 - (i / 28) * (29 / (i + 1)) * ((21 - n) / 11))
        j = y + y / 4 + i + 2 - c + c / 4
        j = j - 7 * (j / 7)
        l = i - j
        m = 3 + (l + 40) / 44
        d = l + 28 - 31 * (m / 4)

        tl[MONTH] = m
        tl[DAY] = d
        return self.returnwrapper(tl)

    @property
    def martin_luther_king_day(self):
        '''3rd Monday in Jan'''
        tl = copy(self.timelist)
        tl[MONTH] = JAN
        tl[DAY] = nth_day_of_month(3, MON, JAN, tl[YEAR])
        return self.returnwrapper(tl)

    # Jewish holidays begin the evening before the first day of the holiday
    # therefor each function, set_holiday() returns the first day
    # and the function set_holiday_eve() returns the prior day.
    @property
    def hanukkah(self):
        '''need an algorithm to compute gregorian first day...'''
        tl = copy(self.timelist)
        gd = hebrew.to_jd_gregorianyear(tl[YEAR], Kislev, 25)
        tl[MONTH] = gd[MONTH]
        tl[DAY] = gd[DAY]
        return self.returnwrapper(tl)

    @property
    def hanukkah_eve(self):
        tl = self.hanukkah
        tl[DAY] -= 1
        tl = adjust_date(tl)
        return self.returnwrapper(tl)

    @property
    def rosh_hashanah(self):
        tl = copy(self.timelist)
        gd = hebrew.to_jd_gregorianyear(tl[YEAR], Tishri, 1)
        tl[MONTH] = gd[MONTH]
        tl[DAY] = gd[DAY]
        return self.returnwrapper(tl)

    @property
    def rosh_hashanah_eve(self):
        tl = self.rosh_hashanah
        tl[DAY] -= 1
        tl = adjust_date(tl)
        return self.returnwrapper(tl)

    @property
    def yom_kippur(self):
        tl = copy(self.timelist)
        gd = hebrew.to_jd_gregorianyear(tl[YEAR], Tishri, 10)
        tl[MONTH] = gd[MONTH]
        tl[DAY] = gd[DAY]
        return self.returnwrapper(tl)

    @property
    def yom_kippur_eve(self):
        tl = self.rosh_hashanah
        tl[DAY] += 8
        tl = adjust_date(tl)
        return self.returnwrapper(tl)

    @property
    def passover(self):
        tl = copy(self.timelist)
        gd = hebrew.to_jd_gregorianyear(tl[YEAR], Nisan, 15)
        tl[MONTH] = gd[MONTH]
        tl[DAY] = gd[DAY]
        return self.returnwrapper(tl)

    @property
    def passover_eve(self):
        tl = self.passover
        tl[DAY] -= 1
        tl = adjust_date(tl)
        return self.returnwrapper(tl)


if __name__ == '__main__':
    holiday = Holidays(2014)
