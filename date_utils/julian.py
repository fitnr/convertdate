# -*- coding: utf-8 -*-
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
import astro

import bahai
import french_republican
import gregorian
import hebrew
import iso
import mayan
import islamic
import persian

J0000 = 1721424.5  # // Julian date of Gregorian epoch: 0000-01-01
J1970 = 2440587.5  # // Julian date at Unix epoch: 1970-01-01
JMJD = 2400000.5  # // Epoch of Modified Julian Date system

JULIAN_EPOCH = 1721423.5


class Julianday(float):

    def floor(self):
        # the python math module astro.floor func returns a float
        return int(self)

    @property
    def gregorian(jd):
        wjd = astro.floor(jd - 0.5) + 0.5
        depoch = wjd - gregorian.EPOCH
        quadricent = astro.floor(depoch / 146097)
        dqc = depoch % 146097
        cent = astro.floor(dqc / 36524)
        dcent = dqc % 36524
        quad = astro.floor(dcent / 1461)
        dquad = dcent % 1461
        yindex = astro.floor(dquad / 365)
        year = (quadricent * 400) + (cent * 100) + (quad * 4) + yindex
        if not (cent == 4 or yindex == 4):
            year += 1
        yearday = wjd - gregorian.to_jd(year, 1, 1)
        if wjd < gregorian.to_jd(year, 3, 1):
            leap_adj = 0
        elif gregorian.leap(year):
            leap_adj = 1
        else:
            leap_adj = 2
        month = astro.floor((((yearday + leap_adj) * 12) + 373) / 367)
        day = int(wjd - gregorian.to_jd(year, month, 1)) + 1
        return (year, month, day)

    @property
    def hebrew(jd):
        jd = jd.floor() + 0.5
        count = astro.floor(((jd - hebrew.EPOCH) * 98496.0) / 35975351.0)
        year = count - 1
        i = count
        while jd >= hebrew.to_jd(i, 7, 1):
            i += 1
            year += 1

        if jd < hebrew.to_jd(year, 1, 1):
            first = 7
        else:
            first = 1

        month = i = first
        while jd > hebrew.to_jd(year, i, hebrew.month_days(year, i)):
            i += 1
            month += 1

        day = int(jd - hebrew.to_jd(year, month, 1)) + 1
        return (year, month, day)

    @property
    def iso(jd):
        #//  JD_TO_ISO  --  Return tuple of ISO (year, week, day) for Julian day
        year = Julianday(jd - 3).gregorian[0]
        if jd >= iso.to_julian(year + 1, 1, 1):
            year += 1
        week = astro.floor((jd - iso.to_julian(year, 1, 1)) / 7) + 1
        day = astro.jwday(jd)
        if day == 0:
            day = 7

        return (year, week, day)

    @property
    def iso_day(jd):
        #//  JD_TO_ISO_DAY  --  Return tuple of ISO (year, day_of_year) for Julian day
        year = jd.gregorian[0]
        day = astro.floor(jd - gregorian.to_jd(year, 1, 1)) + 1
        return (year, day)

    @property
    def julian(td):
        #//  JD_TO_JULIAN  --  Calculate Julian calendar date from Julian day

        td += 0.5
        z = astro.floor(td)

        a = z
        b = a + 1524
        c = astro.floor((b - 122.1) / 365.25)
        d = astro.floor(365.25 * c)
        e = astro.floor((b - d) / 30.6001)

        if astro.floor(e < 14):
            month = e - 1
        else:
            month = e - 13

        if astro.floor(month > 2):
            year = c - 4716
        else:
            year = c - 4715

        day = b - d - astro.floor(30.6001 * e)

        #/*  If year is less than 1, subtract one to convert from
        #    a zero based date system to the common era system in
        #    which the year -1 (1 B.C.E) is followed by year 1 (1 C.E.).  */

        if year < 1:
            year -= 1

        return (year, month, day)

    @property
    def french_republican(jd):
        '''Calculate date in the French Revolutionary
        calendar from Julian day.  The five or six
        "sansculottides" are considered a thirteenth'''
        # month in the results of this function.  */
        jd = Julianday(astro.floor(jd) + 0.5)
        adr = french_republican.annee_da_la_revolution(jd)
        an = int(adr[0])
        equinoxe = adr[1]
        mois = astro.floor((jd - equinoxe) / 30) + 1
        jour = (jd - equinoxe) % 30
        decade = astro.floor(jour / 10) + 1
        jour = int(jour % 10) + 1

        return (an, mois, decade, jour)

    @property
    def islamic(jd):
        '''Calculate Islamic date from Julian day'''

        jd = astro.floor(jd) + 0.5
        year = astro.floor(((30 * (jd - islamic.EPOCH)) + 10646) / 10631)
        month = min(12,
                    astro.ceil((jd - (29 + islamic.to_jd(year, 1, 1))) / 29.5) + 1)
        day = int(jd - islamic.to_jd(year, month, 1)) + 1
        return (year, month, day)

    @property
    def persian(jd):
        '''Calculate Persian date from Julian day'''
        jd = astro.floor(jd) + 0.5

        depoch = jd - persian.to_jd(475, 1, 1)
        cycle = astro.floor(depoch / 1029983)
        cyear = (depoch % 1029983)
        if cyear == 1029982:
            ycycle = 2820
        else:
            aux1 = astro.floor(cyear / 366)
            aux2 = (cyear % 366)
            ycycle = astro.floor(
                ((2134 * aux1) + (2816 * aux2) + 2815) / 1028522) + aux1 + 1

        year = ycycle + (2820 * cycle) + 474
        if (year <= 0):
            year -= 1

        yday = (jd - persian.to_jd(year, 1, 1)) + 1
        if yday <= 186:
            month = astro.ceil(yday / 31)
        else:
            month = astro.ceil((yday - 6) / 30)

        day = int(jd - persian.to_jd(year, month, 1)) + 1
        return (year, month, day)

    @property
    def mayan_count(jd):
        '''Calculate Mayan long count from Julian day'''
        d = jd - mayan.EPOCH
        baktun = astro.floor(d / 144000)
        d = (d % 144000)
        katun = astro.floor(d / 7200)
        d = (d % 7200)
        tun = astro.floor(d / 360)
        d = (d % 360)
        uinal = astro.floor(d / 20)
        kin = int((d % 20))

        return (baktun, katun, tun, uinal, kin)

    @property
    def mayan_haab(jd):
        '''Determine Mayan Haab "month" and day from Julian day'''
        lcount = jd - mayan.EPOCH
        day = (lcount + 8 + ((18 - 1) * 20) % 365)

        return (astro.floor(day / 20) + 1, int((day % 20)))

    @property
    def mayan_tzolkin(jd):
        '''Determine Mayan Tzolkin "month" and day from Julian day'''
        lcount = jd - mayan.EPOCH
        return (int(astro.amod(lcount + 20, 20)), int(astro.amod(lcount + 4, 13)))

    @property
    def bahai(jd):
        '''Calculate Bahai date from Julian day'''

        jd = Julianday(jd.floor() + 0.5)
        gy = jd.gregorian[0]
        bstarty = Julianday(bahai.EPOCH).gregorian[0]

        if jd <= gregorian.to_jd(gy, 3, 20):
            x = 1
        else:
            x = 0
        # verify this next line...
        bys = gy - (bstarty + (((gregorian.to_jd(gy, 1, 1) <= jd) and x)))
        major = astro.floor(bys / 361) + 1
        cycle = astro.floor((bys % 361) / 19) + 1
        year = (bys % 19) + 1
        days = jd - bahai.to_jd(major, cycle, year, 1, 1)
        bld = bahai.to_jd(major, cycle, year, 20, 1)
        if jd >= bld:
            month = 20
        else:
            month = astro.floor(days / 19) + 1
        day = int((jd + 1) - bahai.to_jd(major, cycle, year, month, 1))

        return (major, cycle, year, month, day)

    @property
    def indian_civil(jd):
        '''Calculate Indian Civil date from Julian day
        Offset in years from Saka era to Gregorian epoch'''

        Saka = 79 - 1
        start = 80
        # // Day offset between Saka and Gregorian

        jd = Julianday(jd.floor() + 0.5)
        greg = jd.gregorian  # // Gregorian date for Julian day
        leap = gregorian.leap(greg[0])  # // Is this a leap year?
        year = greg[0] - Saka  # // Tentative year in Saka era
        # // JD at start of Gregorian year
        greg0 = gregorian.to_jd(greg[0], 1, 1)
        yday = jd - greg0  # // Day number (0 based) in Gregorian year

        if leap:
            Caitra = 31  # // Days in Caitra this year
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
                month = astro.floor(mday / 31) + 2
                day = (mday % 31) + 1
            else:
                mday -= 31 * 5
                month = astro.floor(mday / 30) + 7
                day = (mday % 30) + 1

        return (year, month, int(day))


def leap(year):
    if year % 4 and year > 0:
        return 0
    else:
        return 3


def to_jd(year, month, day):
    #/* Adjust negative common era years to the zero-based notation we use.  */

    if year < 1:
        year += 1

    #/* Algorithm as given in Meeus, Astronomical Algorithms, Chapter 7, page 61 */

    if month <= 2:
        year -= 1
        month += 12

    return Julianday((astro.floor((365.25 * (year + 4716))) +
                      astro.floor((30.6001 * (month + 1))) +
                      day) - 1524.5)


def verify(jd, func, args_tuple):

    jd_cmp = func(*args_tuple)

    if jd != jd_cmp:
        e = "ERROR: {0}({1}) = {2} did not match jd ({3})"
        raise e.format(func, args, jd_cmp, jd)
    else:
        return 1


if __name__ == '__main__':
    import sys
    import time

    args = sys.argv[1:]

    if len(args) < 3:
        tm = time.localtime()
        gregoriandate = (tm[0], tm[1], tm[2])
    else:
        gregoriandate = (int(args[0]), int(args[1]), int(args[2]))

    print "\nRunning date conversion test script:"
    print "-------------------------------------"

    print "gregorian date:", gregoriandate

    jd = gregorian.to_jd(gregoriandate[0], gregoriandate[1], gregoriandate[2])

    print "julian day:", jd

    cals = ('hebrew', 'islamic', 'persian', 'indian_civil', 'iso',
            'iso_day', 'julian', 'mayan_count', 'mayan_haab',
            'mayan_tzolkin', 'bahai', 'french_republican')

    errors = 0
    for cal in cals:
        val = getattr(jd, cal)
        print "%s: %s" % (cal, val)

        try:
            func = eval("{0}_to_jd".format(cal))

            assert type(jd) == Julianday

            assert verify(jd, func, val) == 1

        except NameError:
            # print str(func), "does not exist"
            pass

    if errors:
        print "\nEncountered", errors, "errors in converting to and from jd"
    else:
        print "\nDate conversion tests completed successfully"
