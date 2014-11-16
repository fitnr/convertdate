# -*- coding: utf-8 -*-
from copy import copy
import unittest
from convertdate import dublin
from convertdate import julian
from convertdate import gregorian
from convertdate import babylonian as bab
from convertdate.data import babylonian_data as data
import ephem
from random import randint
from math import trunc


class test_babylon_cal(unittest.TestCase):

    def setUp(self):
        self.string = "{jyear}\t{jdate}\t{daysinyear}\t{m}\t{ve}\t{nm}"

    def test_metonic(self):
        assert bab.metonic_number(-747) == 1
        assert bab.metonic_number(-440) == 4

        assert bab.metonic_start(-500) == -500
        assert bab.metonic_start(-380) == -386

        assert bab.metonic_start(-576) == -576

        assert bab.metonic_start(1) == -6

        assert bab.metonic_number(1) == 7

        assert bab.metonic_start(-596) == -614
        assert bab.metonic_number(-596) == 19

        self.assertRaises(IndexError, bab.metonic_start, 0)
        self.assertRaises(IndexError, bab.metonic_number, 0)

    def test_intercal_patterns(self):
        assert bab.intercalation(1) == dict(list(zip(list(range(1, 13)), data.MONTHS)))

        leapyear_A = bab.intercalate(-385)
        assert len(leapyear_A) == 13
        assert leapyear_A[13] == u"Addaru II"

        assert len(bab.intercalate(-576)) == 12
        assert len(bab.intercalate(-595)) == 12
        assert len(bab.intercalate(-535)) == 12

        leapyear_U = bab.intercalate(-596)

        assert bab.intercalation_pattern('U') == {
            1: u'Nisannu', 2: u'Aiaru', 3: u'Simanu', 4: u'Duzu', 5: u'Abu', 6: u'Ululu',
            7: u'Ululu II', 8: u'Tashritu', 9: u'Araá¸¥samnu', 10: u'Kislimu', 11: u'á¹¬ebetu',
            12: u'Shabaá¹­u', 13: u'Addaru'}

        assert len(leapyear_U) == 13
        assert leapyear_U[7] == u"Ululu II"

        assert data.intercalations[bab.metonic_start(-596)][bab.metonic_number(-596)] == 'U'

        assert data.intercalations[bab.metonic_start(-596)][bab.metonic_number(-596)] == 'U'

        assert len(leapyear_U) == 13

        assert leapyear_U[7] == u"Ululu II"

        assert len(bab.intercalate(47)) == 12

    def test_valid_regnal(self):
        assert bab._valid_regnal(-500)
        assert bab._valid_regnal(-627) == False
        assert bab._valid_regnal(-145) == False

    def test_bab_regnal_year(self):
        assert bab.regnalyear(-604) == (1, u'Nebuchadnezzar II')
        assert bab.regnalyear(-329) == (8, u'Alexander the Great')
        assert bab.regnalyear(-627) == False

        assert bab.regnalyear(-626) == (0, u'Nabopolassar')
        assert bab.regnalyear(-625) == (1, u'Nabopolassar')
        assert bab.regnalyear(-624) == (2, u'Nabopolassar')
        assert bab.regnalyear(-623) == (3, u'Nabopolassar')
        assert bab.regnalyear(-622) == (4, u'Nabopolassar')
        assert bab.regnalyear(-621) == (5, u'Nabopolassar')

        assert bab.regnalyear(-334) == (2, u'Darius III')

    def test_babylon_from_jd_regnal(self):
        assert bab.from_jd(1492870.5, 'regnal') == ((0, u'Nabopolassar'), u"Nisannu", 1)
        assert bab.from_julian(-330, 7, 30, 'regnal') == ((7, u'Alexander the Great'), u'Abu', 1)

        self.assertRaises(IndexError, bab.from_julian, -626, 4, 1)

    def test_babylon_from_jd_seleucid(self):
        assert bab.from_julian(-6, 4, 20, 'seleucid') == (306, u'Nisannu', 1)
        assert bab.from_julian(-6, 3, 22, 'seleucid') == (305, u"Addaru II", 1)

        assert bab.from_julian(40, 4, 2, 'seleucid') == (351, u'Nisannu', 1)

        assert bab.from_julian(45, 4, 8, 'seleucid') == (356, u'Nisannu', 1)
        assert bab.from_julian(45, 3, 10, 'seleucid') == (355, u"Addaru", 2)

        assert bab.from_julian(45, 11, 30, 'seleucid') == (356, u"Kislimu", 1)

        assert bab.from_julian(46, 2, 26, 'seleucid') == (356, u"Addaru", 1)

    def test_prev_visible_nm(self):
        dc = dublin.from_gregorian(2014, 11, 25)
        self.assertEqual(bab.previous_visible_nm(dc).tuple(), (2014, 11, 22, 0, 0, 0))

    def test_babylon_from_jd_analeptic(self):
        self.assertEqual(bab.from_julian(46, 3, 27, 'seleucid'), (357, u'Nisannu', 1))

        self.assertEqual(bab.from_julian(100, 3, 2), (410, u'Addaru', 3))
        self.assertEqual(bab.from_julian(100, 4, 2), (411, u'Nisannu', 4))
        self.assertEqual(bab.from_julian(100, 5, 1), (411, u'Aiaru', 4))
        self.assertEqual(bab.from_julian(100, 6, 1), (411, u'Simanu', 5))

        cjs = [
            1738298,
            1738357,
            1738387,
            1738416,
            1738475,
            1738504,
            1738534,
            1738563,
            1738593,
            1738622,
        ]

        for x in cjs:
            bab.from_jd(x - 1, plain=1)
            one = bab.from_jd(x, plain=1)
            two = bab.from_jd(x + 1, plain=1)

            assert one[0] <= two[0]

            assert one != two

            if one[2] not in [28, 29, 30]:
                assert one[2] + 1 == two[2]

        self.assertEqual(bab.from_gregorian(2014, 11, 7, plain=1), (2325, 'Arahsamnu', 15))

    def test_load_parker_dubberstein(self):
        bab.load_parker_dubberstein()
        parkerdub = bab.PARKER_DUBBERSTEIN

        assert parkerdub[-604].get('months')
        assert parkerdub[-581].get('months').get(6) == julian.to_jd(-581, 9, 12)

    def test_year_lengths_parker_dubberstein(self):
        parkerdub = bab.PARKER_DUBBERSTEIN

        for year in list(range(-311, -1)) + list(range(1, 41)):
            diy = days_in_year(parkerdub, year)

            monlen = len(bab.intercalate(year))

            self.assertGreater(diy, monlen * 29)
            self.assertLess(diy, monlen * 30)

    def test_year_starts(self):
        for x in range(1700, 2000):
            pev = bab._nvnm_after_pve(ephem.Date(str(x) + '/6/1'))
            nex = bab._nvnm_after_pve(ephem.Date(str(x + 1) + '/6/1'))

            diy = round(nex - pev, 1)
            monlen = len(bab.intercalate(x))

            self.assertGreater(diy, monlen * 29)
            self.assertLess(diy, monlen * 30)


    def test_year_lengths_analeptic(self):
        for year in range(2000, 2200):
            start = bab.to_jd(year, 'Nisannu', 1)
            monlen = len(bab.intercalate(gregorian.from_jd(start)[0]))
            end = bab.to_jd(year, monlen, 30)

            self.assertLess(end - start, monlen * 30)
            self.assertGreater(end - start, monlen * 29)

    def test_metonic_cycle(self):
        dc = dublin.from_gregorian(1900, 3, 19)
        nve = ephem.next_vernal_equinox(dc)
        metonic_months = count_pattern(nve)

        assert len(metonic_months) == 19
        assert sum(metonic_months) == 235

    def test_bab_to_julian_seleucid(self):
        assert bab.to_julian(1, 1, 1, era='seleucid') == (-311, 4, 3)
        assert bab.to_julian(312, 1, 1, era='seleucid') == (1, 4, 14)
        assert bab.to_julian(311, 2, 3, era='seleucid') == (-1, 4, 26)

        assert bab.to_julian(311, 12, 1, era='seleucid') == (1, 2, 14)
        assert bab.to_julian(311, 12, 5, era='seleucid') == (1, 2, 18)
        assert bab.to_julian(327, 1, 1, era='seleucid') == (16, 3, 29)

    def test_bab_to_julian_arsacid(self):
        assert bab.to_julian(1, 1, 1, era='arsacid') == (-247, 4, 15)
        assert bab.to_julian(2, 1, 1, era='arsacid') == (-246, 4, 4)
        assert bab.to_julian(22, 1, 1, era='arsacid') == (-226, 4, 22)
        assert bab.to_julian(232, 1, 1, era='arsacid') == (-16, 4, 11)
        assert bab.to_julian(142, 1, 1, era='arsacid') == (-106, 4, 17)
        assert bab.to_julian(242, 1, 1, era='arsacid') == (-6, 4, 20)
        assert bab.to_julian(263, 1, 1, era='arsacid') == (16, 3, 29)

    def test_bab_to_julian_regnal(self):
        self.assertRaises(ValueError, bab.to_julian, 1, 1, 1, era='regnal')
        assert bab.to_julian(1, 13, 1, era='regnal', ruler='Nabunaid') == (-554, 3, 20)
        assert bab.to_julian(1, 13, 10, era='regnal', ruler='Nabunaid') == (-554, 3, 29)

        assert bab.to_julian(3, 12, 1, era='regnal', ruler='Cyrus') == (-535, 2, 19)

        assert bab.to_julian(4, 13, 1, era='regnal', ruler='Nebuchadnezzar II') == (-600, 3, 18)

        assert bab.to_julian(0, 1, 1, era='regnal', ruler='Nabopolassar') == (-626, 4, 5)

        self.assertEqual(bab.to_julian(1, 1, 1, era='regnal', ruler='Nabopolassar'), (-625, 3, 24))

        assert bab.to_julian(21, 10, 1, era='regnal', ruler='Nabopolassar') == (-604, 1, 3)

    def test_moons_between_dates(self):
        d1 = ephem.Date('2014/11/1')

        assert bab.moons_between_dates(d1, ephem.Date('2014/12/1')) == 1
        assert bab.moons_between_dates(d1, d1 + 1) == 0
        assert bab.moons_between_dates(ephem.Date('2014/11/20'), ephem.Date('2014/11/25')) == 1

    def test_bab_to_jd(self):
        z = gregorian.to_jd(1900, 3, 19)

        for x in range(0, 1000, 20):
            w = bab.to_jd(*bab.from_jd(z + x))
                # print((u"{}\t{}\t{}\t{}\t{}\t{}".format((z + x), w, w - z - x, *bab.from_jd(z + x, plain=1))))

            self.assertEqual((z + x), bab.to_jd(*bab.from_jd(z + x)))

        assert bab.to_jd(*bab.from_jd(z)) == z

    # def test_limits_of_metonic(self):
    #     print('test_limits_of_metonic')
    #     for y in list(range(-595, 0, 38)) + list(range(14, 4000, 38)):
    #         vnm = bab._nvnm_after_pve(ephem.Date(str(y) + '/6/1'))
    #         print('*', y, round(vnm - ephem.previous_vernal_equinox(str(y) + '/6/1')), bab.from_gregorian(y, vnm.datetime().month, vnm.datetime().day))

    #     moon = ephem.next_new_moon('128/4/15')
    #     for x in range(1, 237):
    #         pve = ephem.previous_vernal_equinox(moon)
    #         if moon - pve < 29.5:
    #             v = pve
    #         else:
    #             v = ''

    #         m = bab.metonic_number(moon.datetime().year)

    #         if moon.datetime().year > pve.datetime().year:
    #             m -= 1

    #         # print("{}\t{}\t{}\t{}".format(x, m, moon, v))
    #         moon = ephem.next_new_moon(moon)

    # def test_na1(self):
    #     for u, v in d:
    #         print u, v

    #     print('nvnm', bab.next_visible_nm(ephem.Date('2014/3/19')))

    #     babylon = bab.observer()
    #     sun = ephem.Sun()
    #     moon = ephem.Moon()
    #     print('moons NA1')
    #     nnm = ephem.next_new_moon(1)

    #     print('x, moon.alt, sun.alt')
    #     for x in range(1, 100):
    #         babylon.date = nnm = ephem.next_new_moon(nnm)
    #         babylon.date = babylon.next_setting(sun)
    #         moon.compute(babylon)

    #         if moon.alt < 0:
    #             babylon.date = babylon.next_setting(sun)
    #             print('moon alt %s' % round(moon.alt * 57.2957795))

    #     print("{}\t{}\t{}".format(x, round(moon.alt * 57.2957795), round(sun.az * 57.2957795)))

    def test_overall_days_of_month(self):

        # nnm = ephem.next_new_moon(10)

        # for x in range(1, 100):
        #     pnm = nnm
        #     nnm = ephem.next_new_moon(pnm)
        #     pvnm = bab.previous_visible_nm(nnm)
        #     nvnm = bab.next_visible_nm(pnm)
        #     print(round(nnm - pnm, 2), round(nvnm - pvnm, 2))

        r = randint(1757584, 2450544)
        for x in range(r, r + 10000, 30):
            dc = dublin.from_jd(x)
            nvnm = bab.next_visible_nm(dc)
            pvnm = bab.previous_visible_nm(dc)
            assert round(nvnm - pvnm, 0) in [29.0, 30.0, 29, 30]


def thing(jdc):
    '''jdc should be the first day of a bab year'''
    jy, jm, jd = julian.from_jd(jdc)
    dc = dublin.from_jd(jdc)
    midyear = dublin.from_julian(jy, 5, 1)

    days_since_ve = dc - ephem.previous_vernal_equinox(midyear)
    days_since_nm = dc - ephem.previous_new_moon(dc)

    return {
        'jyear': jy,
        'jdate': '{}-{}'.format(jm, jd),
        've': round(days_since_ve, 2),
        'nm': round(days_since_nm, 2),
        'm': bab.metonic_number(jy)
    }


def analeptic_start_of_year(gyear):
    ddate = ephem.Date(str(gyear) + '/5/1')
    nnm = bab._nvnm_after_pve(ddate + 3)
    babdate = bab.from_gregorian(*dublin.to_gregorian(nnm))

    if babdate[1] != 'Nisannu':
        nnm = nnm + 30
        babdate = bab.from_gregorian(*dublin.to_gregorian(nnm), plain=1)

    while babdate[2] != 1:
        if babdate[2] > 1:
            nnm = nnm - 1
            babdate = bab.from_gregorian(*dublin.to_gregorian(nnm), plain=1)

    return dublin.to_jd(nnm)


def analeptic_thing(gyear):
    return thing(analeptic_start_of_year(gyear))


def days_in_year(parkerdub, jyear):
    '''Return the number of days in the bab. year that overlaps this JY'''
    return parkerdub[jyear + 1]['months'][1] - parkerdub[jyear]['months'][1]


def _analeptic_days_in_year(gyear):
    month = len(bab.intercalate(gyear))
    firstmoon = moon = bab._nvnm_after_pve(ephem.Date(str(gyear) + '/5/1'))

    for x in range(1, 1 + month):
        # print x, moon
        moon = ephem.next_new_moon(moon)

    return round(moon - firstmoon)


def days_btw_ve(jyear):
    yearve = ephem.previous_vernal_equinox(dublin.from_julian(jyear, 6, 6))
    nextve = ephem.previous_vernal_equinox(dublin.from_julian(jyear + 1, 6, 6))
    return nextve - yearve


def count_moons_between_ve(startyear):
    '''Starting at a year, count the number of moons between vernal equinoxes for next 19 years'''
    startdate = ephem.Date(str(startyear) + '/1/1')
    enddate = ephem.Date(str(startyear + 19) + '/1/1')

    ve = ephem.next_vernal_equinox(startdate)
    years = {}

    while ve < enddate:
        nve = ephem.next_vernal_equinox(ve + 1)
        years[ve.datetime().year] = bab.moons_between_dates(ve, nve)
        ve = nve

    return years


def count_pattern(startingve):
    # days until ve.
    ve = copy(startingve)
    nnm = copy(startingve)

    metonic = {}

    for x in range(19):
        ve = ephem.next_vernal_equinox(ve)
        metonic[ve] = []

        while nnm < ve - 30:
            nnm = ephem.next_new_moon(nnm)
            metonic[ve].append(ephem.date(nnm))

    metonic_months = []

    for months in list(metonic.values()):
        metonic_months.append(len(months))

    return metonic_months


if __name__ == '__main__':
    unittest.main()
