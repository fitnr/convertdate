#  calendar_util.py: -*- Python -*-  DESCRIPTIVE TEXT.
#  
#  Author: Phil Schwartz (phil_schwartz@users.sourceforge.net) 
#  Date: Tue Jan 14 10:22:35 2003.
#
# Most of this code is ported from Fourmilab's javascript calendar converter
# http://www.fourmilab.ch/documents/calendar/
# which was developed by John Walker
#
# The algorithms are believed to be derived from the following source:
# Meeus, Jean. Astronomical Algorithms . Richmond: Willmann-Bell, 1991. ISBN 0-943396-35-2. 
#    The essential reference for computational positional astronomy. 
#
from astro import *


J0000 = 1721424.5                #// Julian date of Gregorian epoch: 0000-01-01
J1970 = 2440587.5                #// Julian date at Unix epoch: 1970-01-01
JMJD  = 2400000.5                #// Epoch of Modified Julian Date system

GREGORIAN_EPOCH = 1721425.5
HEBREW_EPOCH = 347995.5
JULIAN_EPOCH = 1721423.5
FRENCH_REVOLUTIONARY_EPOCH = 2375839.5
ISLAMIC_EPOCH = 1948439.5
ISLAMIC_WEEKDAYS = ("al-'ahad", "al-'ithnayn",
                    "ath-thalatha'", "al-'arb`a'",
                    "al-khamis", "al-jum`a", "as-sabt")
PERSIAN_EPOCH = 1948320.5
PERSIAN_WEEKDAYS = ("Yekshanbeh", "Doshanbeh",
                    "Seshhanbeh", "Chaharshanbeh",
                    "Panjshanbeh", "Jomeh", "Shanbeh")
MAYAN_COUNT_EPOCH = 584282.5
MAYAN_HAAB_MONTHS = ("Pop", "Uo", "Zip", "Zotz", "Tzec", "Xul",
                     "Yaxkin", "Mol", "Chen", "Yax", "Zac", "Ceh",
                     "Mac", "Kankin", "Muan", "Pax", "Kayab", "Cumku")
 
MAYAN_TZOLKIN_MONTHS = ("Imix", "Ik", "Akbal", "Kan", "Chicchan",
                        "Cimi", "Manik", "Lamat", "Muluc", "Oc",
                        "Chuen", "Eb", "Ben", "Ix", "Men",
                        "Cib", "Caban", "Etxnab", "Cauac", "Ahau")
 
BAHAI_EPOCH = 2394646.5
BAHAI_WEEKDAYS = ("Jamál", "Kamál", "Fidál", "Idál",
                               "Istijlál", "Istiqlál", "Jalál")
INDIAN_CIVIL_WEEKDAYS = ("ravivara", "somavara", "mangalavara", "budhavara",
                         "brahaspativara", "sukravara", "sanivara")

Weekdays = ( "Sunday", "Monday", "Tuesday", "Wednesday",
             "Thursday", "Friday", "Saturday" )




def leap_gregorian(year):
    return (year % 4 == 0 and
            not ((year % 100) == 0 and (year % 400) != 0))


def gregorian_to_jd(year, month, day):
    if month <= 2:
        leap_adj = 0
    elif leap_gregorian(year):
        leap_adj = -1
    else:
        leap_adj = -2

    return ((GREGORIAN_EPOCH - 1) +
           (365 * (year - 1)) +
           floor((year - 1) / 4) +
           (-floor((year - 1) / 100)) +
           floor((year - 1) / 400) +
           floor((((367 * month) - 362) / 12) +
           leap_adj +
           day))


def jd_to_gregorian(jd):
    wjd = floor(jd - 0.5) + 0.5
    depoch = wjd - GREGORIAN_EPOCH
    quadricent = floor(depoch / 146097)
    dqc = mod(depoch, 146097)
    cent = floor(dqc / 36524)
    dcent = mod(dqc, 36524)
    quad = floor(dcent / 1461)
    dquad = mod(dcent, 1461)
    yindex = floor(dquad / 365)
    year = (quadricent * 400) + (cent * 100) + (quad * 4) + yindex
    if not (cent == 4 or yindex == 4):
        year +=1

    yearday = wjd - gregorian_to_jd(year, 1, 1)
    if wjd < gregorian_to_jd(year, 3, 1):
        leap_adj = 0
    elif leap_gregorian(year):
        leap_adj = 1
    else:
        leap_adj = 2

    month = floor((((yearday + leap_adj) * 12) + 373) / 367)
    day = int(wjd - gregorian_to_jd(year, month, 1)) + 1
    return (year, month, day)


def hebrew_leap(year):
    #//  Is a given Hebrew year a leap year ?
    return mod(((year * 7) + 1), 19) < 7


def hebrew_year_months(year):
    #//  How many months are there in a Hebrew year (12 = normal, 13 = leap)
    if hebrew_leap(year):
        return 13
    else:
        return 12


def hebrew_delay_1(year):
    #//  Test for delay of start of new year and to avoid
    #//  Sunday, Wednesday, and Friday as start of the new year.
    months = ((235 * year) - 234) / 19
    parts = 12084 + (13753 * months)
    day = (months * 29) + parts / 25920

    if mod((3 * (day + 1)), 7) < 3:
        day += 1

    return day



def hebrew_delay_2(year):
    #//  Check for delay in start of new year due to length of adjacent years

    last = hebrew_delay_1(year - 1)
    present = hebrew_delay_1(year)
    next = hebrew_delay_1(year + 1)

    if next - present == 356:
        return 2
    elif present - last == 382:
        return 1
    else:
        return 0


def hebrew_year_days(year):
    #//  How many days are in a Hebrew year ?
    return hebrew_to_jd(year + 1, 7, 1) - hebrew_to_jd(year, 7, 1)


def hebrew_month_days(year, month):
    #//  How many days are in a given month of a given year{

    #//  First of all, dispose of fixed-length 29 day months
    if month in (2,4,6,10,13):
        return 29

    #//  If it's not a leap year, Adar has 29 days
    if month == 12 and not hebrew_leap(year):
        return 29

    #//  If it's Heshvan, days depend on length of year
    if month == 8 and not (mod(hebrew_year_days(year), 10) == 5):
        return 29


    #//  Similarly, Kislev varies with the length of year
    if month == 9 and mod(hebrew_year_days(year), 10) == 3:
        return 29


    #//  Nope, it's a 30 day month
    return 30



def hebrew_to_jd(year, month, day):
    months = hebrew_year_months(year);
    jd = HEBREW_EPOCH + hebrew_delay_1(year) + hebrew_delay_2(year) + day + 1

    if month < 7 :
        for mon in range (7, months+1):
            jd +=  hebrew_month_days(year, mon)

        for mon in range(1, month):
            jd +=  hebrew_month_days(year, mon)
    else:
        for mon in range(7, month):
            jd += hebrew_month_days(year, mon)

    return jd


def jd_to_hebrew(jd):
    jd = floor(jd) + 0.5;
    count = floor(((jd - HEBREW_EPOCH) * 98496.0) / 35975351.0)
    year = count - 1;
    i = count
    while jd >= hebrew_to_jd(i, 7, 1):
        i += 1
        year += 1

    if jd < hebrew_to_jd(year, 1, 1):
        first = 7
    else:
        first = 1

    month = i = first;
    while jd > hebrew_to_jd(year, i, hebrew_month_days(year, i)):
        i += 1
        month += 1

    day = int(jd - hebrew_to_jd(year, month, 1)) + 1
    return (year, month, day)



def weekday_before(weekday, jd):
    return jd - jwday(jd - weekday);



def search_weekday(weekday, jd, direction, offset):
    #/*  SEARCH_WEEKDAY  --  Determine the Julian date for: 
    #        weekday      Day of week desired, 0 = Sunday
    #        jd           Julian date to begin search
    #        direction    1 = next weekday, -1 = last weekday
    #        offset       Offset from jd to begin search
    #*/
    return weekday_before(weekday, jd + (direction * offset))


#//  Utility weekday functions, just wrappers for search_weekday

def nearest_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 3)


def next_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 7)


def next_or_current_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 6)

def previous_weekday(weekday, jd):
    return search_weekday(weekday, jd, -1, 1)


def previous_or_current_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 0)


def n_weeks(weekday, jd, nthweek):
    j = 7 * nthweek

    if nthweek > 0:
        j += previous_weekday(weekday, jd)
    else:
        j += next_weekday(weekday, jd)

    return j

# not sure why the naming converntion for ISO functions use julian rather than jd
def iso_to_jd(year, week, day):
    return iso_to_julian(year, week, day)

def iso_day_to_jd(year, day):
    return iso_day_to_julian(year, day)


def iso_to_julian(year, week, day):
    #//  ISO_TO_JULIAN  --  Return Julian day of given ISO year, week, and day
    return day + n_weeks(0, gregorian_to_jd(year - 1, 12, 28), week)


def jd_to_iso(jd):
    #//  JD_TO_ISO  --  Return tuple of ISO (year, week, day) for Julian day
    year = jd_to_gregorian(jd - 3)[0]
    if jd >= iso_to_julian(year + 1, 1, 1):
        year += 1
    week = floor((jd - iso_to_julian(year, 1, 1)) / 7) + 1
    day = jwday(jd)
    if day == 0:
        day = 7

    return (year, week, day)


def iso_day_to_julian(year, day):
    #//  ISO_DAY_TO_JULIAN  --  Return Julian day of given ISO year, and day of year
    return ((day - 1) + gregorian_to_jd(year, 1, 1))



def jd_to_iso_day(jd):
    #//  JD_TO_ISO_DAY  --  Return tuple of ISO (year, day_of_year) for Julian day
    year = jd_to_gregorian(jd)[0]
    day = floor(jd - gregorian_to_jd(year, 1, 1)) + 1
    return (year, day)


def leap_julian(year):
    if year % 4 and year > 0:
        return 0
    else:
        return 3


def  julian_to_jd(year, month, day):
    #/* Adjust negative common era years to the zero-based notation we use.  */

    if year < 1:
        year += 1

    #/* Algorithm as given in Meeus, Astronomical Algorithms, Chapter 7, page 61 */

    if month <= 2:
        year -= 1
        month += 12

    return ((floor((365.25 * (year + 4716))) +
            floor((30.6001 * (month + 1))) +
            day) - 1524.5)




def jd_to_julian(td):
    #//  JD_TO_JULIAN  --  Calculate Julian calendar date from Julian day

    td += 0.5;
    z = floor(td)

    a = z
    b = a + 1524
    c = floor((b - 122.1) / 365.25)
    d = floor(365.25 * c)
    e = floor((b - d) / 30.6001)

    if floor(e < 14):
        month = e - 1
    else:
        month = e - 13

    if floor(month > 2):
        year = c - 4716
    else:
        year = c - 4715

    day = b - d - floor(30.6001 * e)

    #/*  If year is less than 1, subtract one to convert from
    #    a zero based date system to the common era system in
    #    which the year -1 (1 B.C.E) is followed by year 1 (1 C.E.).  */

    if year < 1:
        year -= 1

    return (year, month, day)


def equinoxe_a_paris(year):
    #/*  EQUINOXE_A_PARIS  --  Determine Julian day and fraction of the
    # September equinox at the Paris meridian in
    # a given Gregorian year.  */
    
    #//  September equinox in dynamical time
    equJED = equinox(year, 2)

    #//  Correct for delta T to obtain Universal time
    equJD = equJED - (deltat(year) / (24 * 60 * 60))
    
    #//  Apply the equation of time to yield the apparent time at Greenwich
    equAPP = equJD + equationOfTime(equJED)
        
    #/*  Finally, we must correct for the constant difference between
    #    the Greenwich meridian and that of Paris, 2°20'15" to the
    #    East.  */ 
    
    dtParis = (2 + (20 / 60.0) + (15 / (60 * 60.0))) / 360
    equParis = equAPP + dtParis
 
    return equParis

    


def paris_equinoxe_jd(year):
    #/*  PARIS_EQUINOXE_JD  --  Calculate Julian day during which the  
    #                           September equinox, reckoned from the Paris
    #                           meridian, occurred for a given Gregorian
    #                           year.  */'
    ep = equinoxe_a_paris(year)
    epg = floor(ep - 0.5) + 0.5

    return epg

        
    

                          
def annee_da_la_revolution(jd):
    #/*  ANNEE_DE_LA_REVOLUTION  --  Determine the year in the French
    #                                revolutionary calendar in which a
    #                                given Julian day falls.  Returns an
    #                                array of two elements:
    #        
    #                                    [0]  Année de la Révolution
    #                                    [1]  Julian day number containing
    #                                         equinox for this year.
    #*/
    guess = jd_to_gregorian(jd)[0] - 2

    lasteq = paris_equinoxe_jd(guess)
    while lasteq > jd:
        guess -= 1
        lasteq = paris_equinoxe_jd(guess)

    nexteq = lasteq - 1
    while not (lasteq <= jd and jd < nexteq):
        lasteq = nexteq
        guess += 1
        nexteq = paris_equinoxe_jd(guess)

    # not sure if python round and javascript math.round behave identically?
    adr = round((lasteq - FRENCH_REVOLUTIONARY_EPOCH) / TropicalYear) + 1
    return (adr, lasteq)

    

def jd_to_french_revolutionary(jd):
    #/*  JD_TO_FRENCH_REVOLUTIONARY  --  Calculate date in the French Revolutionary
    #                                    calendar from Julian day.  The five or six
    #                                    "sansculottides" are considered a thirteenth
    #                                    month in the results of this function.  */
    jd = floor(jd) + 0.5
    adr = annee_da_la_revolution(jd)
    an = int(adr[0])
    equinoxe = adr[1]
    mois = floor((jd - equinoxe) / 30) + 1
    jour = (jd - equinoxe) % 30
    decade = floor(jour / 10) + 1
    jour = int(jour % 10) + 1

    
    return (an, mois, decade, jour)

                                
                                    
def french_revolutionary_to_jd(an, mois, decade, jour):
    #/*  FRENCH_REVOLUTIONARY_TO_JD  --  Obtain Julian day from a given French
    #                                    Revolutionary calendar date.  */
    
    guess = FRENCH_REVOLUTIONARY_EPOCH + (TropicalYear * ((an - 1) - 1))
    adr = (an - 1, 0)

    while adr[0] < an:
        adr = annee_da_la_revolution(guess)
        guess = adr[1] + (TropicalYear + 2)

    equinoxe = adr[1]
    
    jd = equinoxe + (30 * (mois - 1)) + (10 * (decade - 1)) + (jour - 1)
    return jd

    

        
def leap_islamic(year):
    #//  LEAP_ISLAMIC  --  Is a given year a leap year in the Islamic calendar ?
    return (((year * 11) + 14) % 30) < 11
         
    
def islamic_to_jd(year, month, day):
    #//  ISLAMIC_TO_JD  --  Determine Julian day from Islamic date
    return ((day +
            ceil(29.5 * (month - 1)) +
            (year - 1) * 354 +
            floor((3 + (11 * year)) / 30) +
            ISLAMIC_EPOCH) - 1)

    
def jd_to_islamic(jd):
    #//  JD_TO_ISLAMIC  --  Calculate Islamic date from Julian day
        
    jd = floor(jd) + 0.5
    year = floor(((30 * (jd - ISLAMIC_EPOCH)) + 10646) / 10631)
    month = min(12,        
                ceil((jd - (29 + islamic_to_jd(year, 1, 1))) / 29.5) + 1)
    day = int(jd - islamic_to_jd(year, month, 1)) + 1
    return (year, month, day)

 

    
def leap_persian(year):
    #//  LEAP_PERSIAN  --  Is a given year a leap year in the Persian calendar ?
    if year > 0:
        y = 474
    else:
        y = 473

    return ((((((year - y % 2820) + 474) + 38)* 682) % 2816) < 682)
    #return ((((((year - ((year > 0) ? 474 : 473)) % 2820) + 474) + 38) * 682) % 2816) < 682;

        
    

 
def persian_to_jd(year, month, day):
    #//  PERSIAN_TO_JD  --  Determine Julian day from Persian date

    if year >= 0:
        y = 474
    else:
        y =  473
    epbase = year - y
    epyear = 474 + mod(epbase, 2820)

    if month <= 7:
        m = (month - 1) * 31
    else:
        m = (month - 1) * 30 + 6
 
    return (day +
            m +
            floor(((epyear * 682) - 110) / 2816) +
            (epyear - 1) * 365 +
            floor(epbase / 2820) * 1029983 +
            (PERSIAN_EPOCH - 1))

    

            
def jd_to_persian(jd):
    #//  JD_TO_PERSIAN  --  Calculate Persian date from Julian day
    jd = floor(jd) + 0.5
 
    depoch = jd - persian_to_jd(475, 1, 1)
    cycle = floor(depoch / 1029983)
    cyear = mod(depoch, 1029983)
    if cyear == 1029982:
        ycycle = 2820
    else:
        aux1 = floor(cyear / 366)
        aux2 = mod(cyear, 366)
        ycycle = floor(((2134 * aux1) + (2816 * aux2) + 2815) / 1028522) + aux1 + 1

    year = ycycle + (2820 * cycle) + 474
    if (year <= 0):
        year -= 1

    yday = (jd - persian_to_jd(year, 1, 1)) + 1
    if yday <= 186:
        month = ceil(yday / 31)
    else:
        month = ceil((yday - 6) / 30)

    day = int(jd - persian_to_jd(year, month, 1)) + 1
    return (year, month, day)



                                 


def mayan_count_to_jd(baktun, katun, tun, uinal, kin):
    #//  MAYAN_COUNT_TO_JD  --  Determine Julian day from Mayan long count
    return (MAYAN_COUNT_EPOCH +
           (baktun * 144000) +
           (katun  *   7200) +
           (tun    *    360) +
           (uinal  *     20) +
           kin)
                

            
def jd_to_mayan_count(jd):
    #//  JD_TO_MAYAN_COUNT  --  Calculate Mayan long count from Julian day
    d = jd - MAYAN_COUNT_EPOCH;
    baktun = floor(d / 144000)
    d = mod(d, 144000);
    katun = floor(d / 7200)
    d = mod(d, 7200)
    tun = floor(d / 360)
    d = mod(d, 360)
    uinal = floor(d / 20)
    kin = int(mod(d, 20))
    
    return (baktun, katun, tun, uinal, kin)


        
def jd_to_mayan_haab(jd):
    #//  JD_TO_MAYAN_HAAB  --  Determine Mayan Haab "month" and day from Julian day
    lcount = jd - MAYAN_COUNT_EPOCH
    day = mod(lcount + 8 + ((18 - 1) * 20), 365)
     
    return (floor(day / 20) + 1, int(mod(day, 20)))
    

def jd_to_mayan_tzolkin(jd):
    #//  JD_TO_MAYAN_TZOLKIN  --  Determine Mayan Tzolkin "month" and day from Julian day
    lcount = jd - MAYAN_COUNT_EPOCH
    return (int(amod(lcount + 20, 20)), int(amod(lcount + 4, 13)))



def bahai_to_jd(major, cycle, year, month, day):
    #//  BAHAI_TO_JD  --  Determine Julian day from Bahai date
    gy = (361 * (major - 1)) + (19 * (cycle - 1)) + (year - 1) + jd_to_gregorian(BAHAI_EPOCH)[0]

    if month != 20:
        m = 0
    else:
        if leap_gregorian(gy + 1):
            m = -14
        else:
            m = -15
    return (gregorian_to_jd(gy, 3, 20) + (19 * (month - 1)) + m + day)



    
def jd_to_bahai(jd):
    #//  JD_TO_BAHAI  --  Calculate Bahai date from Julian day
    
    jd = floor(jd) + 0.5
    gy = jd_to_gregorian(jd)[0]
    bstarty = jd_to_gregorian(BAHAI_EPOCH)[0]

    if jd <= gregorian_to_jd(gy, 3, 20):
        x = 1
    else:
        x = 0
    # verify this next line...
    bys = gy - (bstarty + (((gregorian_to_jd(gy, 1, 1) <= jd) and x)))
    major = floor(bys / 361) + 1
    cycle = floor(mod(bys, 361) / 19) + 1
    year = mod(bys, 19) + 1
    days = jd - bahai_to_jd(major, cycle, year, 1, 1)
    bld = bahai_to_jd(major, cycle, year, 20, 1)
    if jd >= bld:
        month = 20
    else:
        month = floor(days / 19) + 1
    day = int((jd + 1) - bahai_to_jd(major, cycle, year, month, 1))
    
    return (major, cycle, year, month, day)



def indian_civil_to_jd(year, month, day):
    #//  INDIAN_CIVIL_TO_JD  --  Obtain Julian day for Indian Civil date
           
    gyear = year + 78
    leap = leap_gregorian(gyear);     #// Is this a leap year ?

    # 22 - leap = 21 if leap, 22 non-leap
    start = gregorian_to_jd(gyear, 3, 22 - leap)
    if leap:
        Caitra = 31
    else:
        Caitra = 30
 
    if month == 1:
        jd = start + (day - 1)
    else:
        jd = start + Caitra
        m = month - 2
        m = min(m, 5)
        jd += m * 31
        if month >= 8:
            m = month - 7
            jd += m * 30

        jd += day - 1
 
    return jd

    

 
def jd_to_indian_civil(jd):
    #//  JD_TO_INDIAN_CIVIL  --  Calculate Indian Civil date from Julian day
    Saka = 79 - 1;                    #// Offset in years from Saka era to Gregorian epoch
    start = 80;                       #// Day offset between Saka and Gregorian
    
    jd = floor(jd) + 0.5
    greg = jd_to_gregorian(jd)        #// Gregorian date for Julian day
    leap = leap_gregorian(greg[0])    #// Is this a leap year?
    year = greg[0] - Saka             #// Tentative year in Saka era
    greg0 = gregorian_to_jd(greg[0], 1, 1)    #// JD at start of Gregorian year
    yday = jd - greg0                #// Day number (0 based) in Gregorian year
    
    if leap:
        Caitra = 31           #// Days in Caitra this year
    else:
        Caitra = 30
    
    if yday < start:
        #//  Day is at the end of the preceding Saka year
        year -= 1
        yday += Caitra + (31 * 5) + (30 * 3) + 10 + start


    yday -= start
    if yday < Caitra:
        month = 1
        day = yday + 1
    else:
        mday = yday - Caitra
        if (mday < (31 * 5)):
            month = floor(mday / 31) + 2
            day = (mday % 31) + 1
        else:
            mday -= 31 * 5; 
            month = floor(mday / 30) + 7
            day = (mday % 30) + 1

    return (year, month, int(day))


##########################################################################################



def verify(jd, func, args_tuple):
    
    jd_cmp = apply(func, args_tuple)

    if jd != jd_cmp:
        print "ERROR: %s(%s) = %s did not match jd (%s)" % (func,
                                                            str(args).
                                                            str(jd_cmp),
                                                            str(jd))
        return 0
    else:
        return 1
            
        
if __name__ == '__main__':
    import sys
    import time

    args = sys.argv[1:]
    if len(args) < 3:
        tm = time.localtime()
        gregorian = (tm[0], tm[1], tm[2])
    else:
        gregorian = (int(args[0]), int(args[1]), int(args[2]))

    print "\nRunning date conversion test script:"
    print "-------------------------------------"
    
    print "gregorian date:", gregorian

    jd = gregorian_to_jd(gregorian[0], gregorian[1], gregorian[2])

    print "julian day:", jd

    cals = ('hebrew', 'islamic', 'persian', 'indian_civil', 'iso',
            'iso_day', 'julian', 'mayan_count', 'mayan_haab',
            'mayan_tzolkin', 'bahai', 'french_revolutionary')

    errors = 0
    for cal in cals:
        func = eval("jd_to_%s" % cal)
        val = apply(func, (jd,))
        print "%s: %s" % (cal, str(val))

        try:
            func = eval("%s_to_jd" % cal)
            if not verify(jd, func, val):
                errors += 1
            
        except NameError:
            #print str(func), "does not exist"
            pass
        

            
    if errors:
        print "\nEncountered", errors, "errors in converting to and from jd"
    else:
        print "\nDate conversion tests completed successfully"



    
