#  holidays.py: -*- Python -*-  DESCRIPTIVE TEXT.
#  
#  Author: Phil Schwartz (phil_schwartz@users.sourceforge.net) 
#  Date: Thu Jan  9 20:00:52 2003.

import time
import calendar
import calendar_util

#############################################################################################

# time tuple/list index
YEAR = 0
MONTH = 1
DAY = 2
WEEKDAY = 6

# weekdays
MON=0
TUE=1
WED=2
THU=3
FRI=4
SAT=5
SUN=6

# months
JAN=1
FEB=2
MAR=3
APR=4
MAY=5
JUN=6
JUL=7
AUG=8
SEP=9
OCT=10
NOV=11
DEC=12

# Hebrew months
Nisan=1
Iyyar=2
Sivan=3
Tammuz=4
Av=5
Elul=6
Tishri=7
Heshvan=8
Kislev=9
Teveth=10
Shevat=11
Adar=12
Veadar=13

HEBREW_YEAR_OFFSET = 3760

HAVE_30_DAYS = (APR,JUN,SEP,NOV)
HAVE_31_DAYS = (JAN,MAR,MAY,JUL,AUG,OCT,DEC)

SECONDS_PER_DAY = 60 * 60 * 24


#############################################################################################

class Holidays:
    def __init__(self, year=None):
        self.time_list = list(time.localtime())
        if year:
            self.set_year(year)
        

    def get_epoch(self):
        t = tuple(self.time_list)
        return time.mktime(t)


    def get_tuple(self):
        secs = self.get_epoch()
        return time.localtime(secs)
        #return tuple(self.time_list)

    
    def set_year(self, year):
        self.time_list[YEAR] = year


    def get_nth_day_of_month(self, n, weekday, month, year=None):
        # doesn't set the time list
        # returns the day of the month 1..31
        if not year:
            year = self.time_list[YEAR]

        firstday, daysinmonth = calendar.monthrange(year, month)

        # firstday is MON, weekday is WED -- start with 3rd day of month
        # firstday is WED, weekday is MON --
        # firstday = weekday
        if firstday < weekday:
            date = weekday - firstday + 1 # 2 - 0 + 1
        elif firstday > weekday:
            date = 7 - (firstday - weekday) + 1
        else:
            date = 1

        if n == 1:
            return date

        for i in range(1, n):
            date += 7
            if month in HAVE_30_DAYS and date > 30:
                raise IndexError
            if month in HAVE_31_DAYS and date > 31:
                raise IndexError
            if month == FEB and date > 28:
                ignore, daysinfeb = calendar.monthrange(year, FEB)
                if date > daysinfeb:
                    raise IndexError

        return date


    def hebrew_to_gregorian(self, year, hebrew_month, hebrew_day, year_is_gregorian=1):
        if year_is_gregorian:
            # gregorian year is either 3760 or 3761 years less than hebrew year
            # we'll first try 3760 if conversion to gregorian isn't the same
            # year that was passed to this method, then it must be 3761.
            for y in (year + HEBREW_YEAR_OFFSET, year + HEBREW_YEAR_OFFSET + 1):
                jd = calendar_util.hebrew_to_jd(y, hebrew_month, hebrew_day)
                gd = calendar_util.jd_to_gregorian(jd)
                if gd[YEAR] == year:
                    break
                else:
                    gd = None
        else:
            jd = calendar_util.hebrew_to_jd(year, hebrew_month, hebrew_day)        
            gd = calendar_util.jd_to_gregorian(jd)

        if not gd: # should never occur, but just incase...
            raise RangeError, "Could not determine gregorian year"
        
        return gd # (tuple:  y. m, d))


    def adjust_date(self):
        # after a date calculation, this method will coerce the list members to ensure
        # that they are within the correct bounds.  That is, a date of Oct 32 becomes Nov 1, etc
        tm = (self.time_list[YEAR], self.time_list[MONTH], self.time_list[DAY], 0,0,0,0,0,-1)
        e = time.mktime(tm)
        tm = time.localtime(e)        
        self.time_list[MONTH] = tm[MONTH]
        self.time_list[DAY] = tm[DAY]


    ### the holidays...

    def set_christmas(self, year=None):
        # 25th of December
        if year:
            self.set_year(year)

        self.time_list[MONTH] = DEC
        self.time_list[DAY] = 25

    def set_christmas_eve(self, year=None):
        # 24th of December
        if year:
            self.set_year(year)

        self.time_list[MONTH] = DEC
        self.time_list[DAY] = 24


    def set_thanksgiving(self, year=None):
        # 4th Thursday of Novembet
        if year:
            self.set_year(year)

        self.time_list[MONTH] = NOV
        self.time_list[DAY] = self.get_nth_day_of_month(4, THU, NOV,
                                                        self.time_list[YEAR])

    def set_new_years(self, year=None):
        # Jan 1st
        if year:
            self.set_year(year)

        self.time_list[MONTH] = JAN
        self.time_list[DAY] = 1


    def set_new_years_eve(self, year=None):
        # Dec 31st
        if year:
            self.set_year(year)

        self.time_list[MONTH] = DEC
        self.time_list[DAY] = 31

        
    def set_4th_of_july(self, year=None):
        # July 4th
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = JUL
        self.time_list[DAY] = 4

    def set_flag_day(self, year=None):
        # June 14th
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = JUN
        self.time_list[DAY] = 14


    def set_election_day(self, year=None):
        # 1st Tues in Nov
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = NOV
        self.time_list[DAY] = self.get_nth_day_of_month(1, TUE, NOV,
                                                        self.time_list[YEAR])


    def set_presidents_day(self, year=None):
        # 3rd Monday of Feb
        if year:
            self.set_year(year)

        self.time_list[MONTH] = NOV
        self.time_list[DAY] = self.get_nth_day_of_month(3, MON, FEB,
                                                        self.time_list[YEAR])

    def set_washingtons_birthday(self, year=None):
        # Feb 22
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = FEB
        self.time_list[DAY] = 22


    def set_lincolns_birthday(self, year=None):
        # Feb 12
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = FEB
        self.time_list[DAY] = 12        


    def set_memorial_day(self, year=None):
        # last Monday in May 
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = MAY
        try:
            # if May has 5 Mondays...
            self.time_list[DAY] = self.get_nth_day_of_month(
                5, MON,  MAY, self.time_list[YEAR])
        except IndexError:
            # otherwise, May has only 4 Mondays
            self.time_list[DAY] = self.get_nth_day_of_month(
                4, MON, MAY, self.time_list[YEAR])            


    def set_labor_day(self, year=None):
        # first Monday in Sep
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = SEP
        self.time_list[DAY] = self.get_nth_day_of_month(1, MON, SEP,
                                                        self.time_list[YEAR])

    def set_columbus_day(self, UnitedStates=1, year=None):
        # in USA: 2nd Monday in Oct
        # Elsewhere: Oct 12
        if year:
            self.set_year(year)

        self.time_list[MONTH] = OCT
        if UnitedStates:
            self.time_list[DAY] = self.get_nth_day_of_month(2, MON, OCT,
                                                            self.time_list[YEAR])
        else:
            self.time_list[DAY] = 12


    def set_veterans_day(self, year=None):
        # Nov 11
        if year:
            self.set_year(year)        

        self.time_list[MONTH] = NOV
        self.time_list[DAY] = 11


    def set_valentines_day(self, year=None):
        #feb 14th
        if year:
            self.set_year(year)        

        self.time_list[MONTH] = FEB
        self.time_list[DAY] = 14


    def set_halloween(self, year=None):
        # Oct 31
        if year:
            self.set_year(year)        

        self.time_list[MONTH] = OCT
        self.time_list[DAY] = 31


    def set_mothers_day(self, year=None):
        # 2nd Sunday in May
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = MAY
        self.time_list[DAY] = self.get_nth_day_of_month(2, SUN, MAY,
                                                        self.time_list[YEAR])


    def set_fathers_day(self, year=None):
        # 3rd Sunday in June
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = JUN
        self.time_list[DAY] = self.get_nth_day_of_month(3, SUN, JUN,
                                                        self.time_list[YEAR])        

    def set_easter(self, year=None):
        if year:
            self.set_year(year)

        y = self.time_list[YEAR]
        
        # formula taken from http://aa.usno.navy.mil/faq/docs/easter.html
        c = (y / 100)
        n = y - 19 * ( y / 19 )
        k = ( c - 17 ) / 25
        i = c - c / 4 - ( c - k ) / 3 + 19 * n + 15
        i = i - 30 * ( i / 30 )
        i = i - ( i / 28 ) * ( 1 - ( i / 28 ) * ( 29 / ( i + 1 ) )
                               * ( ( 21 - n ) / 11 ) )
        j = y + y / 4 + i + 2 - c + c / 4
        j = j - 7 * ( j / 7 )
        l = i - j
        m = 3 + ( l + 40 ) / 44
        d = l + 28 - 31 * ( m / 4 )

        self.time_list[MONTH] = m
        self.time_list[DAY] = d


    def set_martin_luther_king_day(self, year=None):
        # 3rd Monday in Jan
        if year:
            self.set_year(year)
            
        self.time_list[MONTH] = JAN
        self.time_list[DAY] = self.get_nth_day_of_month(3, MON, JAN,
                                                        self.time_list[YEAR])
        

    ###### Jewish holidays begin the evening before the first day of the holiday
    ###### therefor each function, set_holiday() returns the first day
    ###### and the function set_holiday_eve() returns the prior day.

    def set_hanukkah(self, year=None):
        # need an algorithm to comute gregorian first day...
        if year:
            self.set_year(year)
            
        gd = self.hebrew_to_gregorian(self.time_list[YEAR], Kislev, 25)
        self.time_list[MONTH] = gd[MONTH]
        self.time_list[DAY] = gd[DAY]
        
    
    def set_hanukkah_eve(self, year=None):
        self.set_hanukkah(year)
        self.time_list[DAY] -= 1
        self.adjust_date()


    def set_rosh_hashanah(self, year=None):
        if year:
            self.set_year(year)

        gd = self.hebrew_to_gregorian(self.time_list[YEAR], Tishri, 1)
        self.time_list[MONTH] = gd[MONTH]
        self.time_list[DAY] = gd[DAY]


    def set_rosh_hashanah_eve(self, year=None):
        self.set_rosh_hashanah(year)
        self.time_list[DAY] -= 1
        self.adjust_date()


    def set_yom_kippur(self, year=None):
        if year:
            self.set_year(year)

        gd = self.hebrew_to_gregorian(self.time_list[YEAR], Tishri, 10)
        self.time_list[MONTH] = gd[MONTH]
        self.time_list[DAY] = gd[DAY]


    def set_yom_kippur_eve(self, year=None):
        self.set_rosh_hashanah(year)
        self.time_list[DAY] += 8
        self.adjust_date()

       
    def set_passover(self, year=None):
        if year:
            self.set_year(year)

        gd = self.hebrew_to_gregorian(self.time_list[YEAR], Nisan, 15)
        self.time_list[MONTH] = gd[MONTH]
        self.time_list[DAY] = gd[DAY]


    def set_passover_eve(self, year=None):
        self.set_passover(year)
        self.time_list[DAY] -= 1
        self.adjust_date()


































##################### old methods

    def set_rosh_hashanah(self, year=None):
        if year:
            self.set_year(year)

        y = self.time_list[YEAR]
        # formula taken from: http://quasar.as.utexas.edu/BillInfo/ReligiousCalendars.html
        # algorithm developed by John Conway
        g = y % 19 + 1 # golden number

        # long formula doesn't seem to work?!?!
        #n = (y/100 - y/400 - 2) + 765433/492480 * (12 * g % 19) + (y % 4)/4 - (313 * y + 89081)/98496
        # short formula only works for 1900-2099, but it seems to work unline the above
        yr = y - 1900 # remove century portion of year
        result = 6.057778996 + 1.554241797 * (12 * g % 19) + 0.25*(yr % 4) - 0.003177794 * yr
        n = int(result)
        fraction = result - n

        # postponement rules:
        # 1.If the day calculated above is a Sunday, Wednesday, or Friday, Rosh Hashanah falls on the next
        #   day (Monday, Thursday or Saturday, respectively).
        # 2.If the calculated day is a Monday, and if the fraction is greater than or equal to 23269/25920,
        #   and if Remainder(12G|19) is greater than 11, Rosh Hashanah falls on the next day, a Tuesday.
        # 3.If it is a Tuesday, and if the fraction is greater than or equal to 1367/2160,
        #   and if Remainder(12G|19) is greater than 6, Rosh Hashanah falls two days
        #   later, on Thursday (NOT WEDNESDAY!!). 
            
        weekday = calendar.weekday(y, SEP, n)
        
        if weekday in (SUN, WED, FRI):
            n += 1
        elif weekday == MON and fraction >= 23269/25920 and 12 * g % 19 > 11:
            n += 1
        elif weekday == TUE and fraction >= 1367/2160 and 12 * g % 19 > 6:
            n += 2

        # September has 30 days... alternatively adjust_date could be called
        if n > 30:
            self.time_list[MONTH] = OCT
            self.time_list[DAY] = n - 30
        else:
            self.time_list[MONTH] = SEP
            self.time_list[DAY] = n

        #print self.time_list[MONTH], self.time_list[DAY]
        


    def set_yom_kippur(self, year=None):
        self.set_rosh_hashanah(year)
        self.time_list[DAY] += 9
        self.adjust_date()
        


    def set_passover(self, year=None):
        # formula taken from: http://quasar.as.utexas.edu/BillInfo/ReligiousCalendars.html
        # algorithm developed by John Conway
        self.set_rosh_hashanah(year)
        m = self.time_list[DAY]
        if self.time_list[MONTH] == OCT:
            m += 30

        self.time_list[MONTH] = MAR
        self.time_list[DAY] = 21 + m
        self.adjust_date()


