# -*- coding: utf-8 -*-
from __future__ import print_function
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
        assert bab.metonic_number(-613) == 1
        assert bab.metonic_number(-440) == 3

        self.assertEqual(bab.metonic_start(-500), -500)
        self.assertEqual(bab.metonic_start(-380), -386)

        self.assertEqual(bab.metonic_start(-576), -576)

        assert bab.metonic_start(1) == -6

        assert bab.metonic_start(19) - bab.metonic_start(1) == 19

        assert bab.metonic_number(1) == 7

        assert bab.metonic_start(-596) == -614
        assert bab.metonic_number(-595) == 0

        assert bab.metonic_number(-292) == 18
        assert bab.metonic_number(374) == 19
        assert bab.metonic_number(375) == 20
        assert bab.metonic_number(376) == 21

    def test_687_year_mega_cycle(self):
        assert len(bab.intercalate(376)) == 13
        assert len(bab.intercalate(1062)) == 12
        assert len(bab.intercalate(1063)) == 13
        assert len(bab.intercalate(1750)) == 13

        monthcount = 0
        count12, count13 = 0, 0
        list12, list13 = [], []

        for y in range(-310, 377):
            l = len(bab.intercalate(y))
            monthcount += l
            if l == 13:
                count13 += 1
                list13.append(y)
            elif l == 12:
                count12 += 1
                list12.append(y)

        self.assertEqual(count13, 253)
        self.assertEqual(count12, 434)
        self.assertEqual(monthcount, 8497)

    def test_intercal_patterns(self):
        assert bab.intercalation(1) == dict(list(zip(list(range(1, 13)), data.MONTHS)))

        leapyear_A = bab.intercalate(-384)
        assert len(leapyear_A) == 13
        assert leapyear_A[13] == u"Addaru II"

        assert len(bab.intercalate(-575)) == 12
        assert len(bab.intercalate(-594)) == 12
        assert len(bab.intercalate(-534)) == 12

        leapyear_U = bab.intercalate(-595)

        self.assertEqual(bab.intercalation_pattern('U'), {
            1: u'Nisannu', 2: u'Aiaru', 3: u'Simanu', 4: u'Duzu', 5: u'Abu', 6: u'Ululu',
            7: u'Ululu II', 8: u'Tashritu', 9: u'Araḥsamnu', 10: u'Kislimu', 11: u'Ṭebetu',
            12: u'Shabaṭu', 13: u'Addaru'})

        self.assertEqual(leapyear_U, bab.intercalation_pattern('U'))

        assert len(leapyear_U) == 13
        assert leapyear_U[7] == u"Ululu II"

        assert data.intercalations[bab.metonic_start(-595)][bab.metonic_number(-595)] == 'U'

        assert data.intercalations[bab.metonic_start(-595)][bab.metonic_number(-595)] == 'U'

        assert len(leapyear_U) == 13

        assert leapyear_U[7] == u"Ululu II"

        assert len(bab.intercalate(47)) == 12

    def test_valid_regnal(self):
        assert bab._valid_regnal(-500)
        assert bab._valid_regnal(-627) == False
        assert bab._valid_regnal(-144) == False

    def test_bab_regnal_year(self):
        assert bab.regnalyear(-603) == (1, u'Nebuchadnezzar II')
        assert bab.regnalyear(-328) == (8, u'Alexander the Great')
        assert bab.regnalyear(-626) == (False, False)

        assert bab.regnalyear(-625) == (0, u'Nabopolassar')
        assert bab.regnalyear(-624) == (1, u'Nabopolassar')
        assert bab.regnalyear(-623) == (2, u'Nabopolassar')
        assert bab.regnalyear(-622) == (3, u'Nabopolassar')
        assert bab.regnalyear(-621) == (4, u'Nabopolassar')
        assert bab.regnalyear(-620) == (5, u'Nabopolassar')

        assert bab.regnalyear(-333) == (2, u'Darius III')

    def test_babylon_from_jd_regnal(self):
        assert bab.from_jd(1492870.5, 'regnal') == (0, u"Nisannu", 1, u'Nabopolassar')
        assert bab.from_julian(-329, 7, 30, 'regnal') == (7, u'Abu', 1, u'Alexander the Great')

        self.assertRaises(IndexError, bab.from_julian, -626, 4, 1)

    def test_julian_jd(self):
        self.assertEqual(bab.from_jd(1721142.5), bab.from_julian(0, 3, 26))

    def test_setting_epoch(self):
        assert bab._set_epoch('seleucid') == data.SELEUCID_EPOCH
        assert bab._set_epoch('arsacid') == data.ARSACID_EPOCH
        assert bab._set_epoch('nabonassar') == data.NABONASSAR_EPOCH
        assert bab._set_epoch('nabopolassar') == data.NABOPOLASSAR_EPOCH

    def test_babylon_from_jd_seleucid(self):
        self.assertEqual(bab.from_julian(1, 4, 14, 'AG'), (312, u'Nisannu', 1, 'AG'))
        self.assertEqual(bab.from_julian(0, 3, 26, 'AG'), (311, u'Nisannu', 1, 'AG'))
        self.assertEqual(bab.from_julian(-1, 4, 7, 'AG'), (310, u'Nisannu', 1, 'AG'))
        self.assertEqual(bab.from_julian(-2, 4, 17, 'AG'), (309, u'Nisannu', 1, 'AG'))
        self.assertEqual(bab.from_julian(-3, 3, 29, 'AG'), (308, u'Nisannu', 1, 'AG'))
        self.assertEqual(bab.from_julian(-4, 4, 8, 'AG'), (307, u'Nisannu', 1, 'AG'))
        self.assertEqual(bab.from_julian(-5, 4, 20, 'AG'), (306, u'Nisannu', 1, 'AG'))
        self.assertEqual(bab.from_julian(-5, 3, 22, 'AG'), (305, u"Addaru II", 1, 'AG'))

        self.assertEqual(bab.from_julian(40, 4, 2, 'seleucid'), (351, u'Nisannu', 1, 'AG'))

        assert bab.from_julian(45, 4, 8, 'seleucid') == (356, u'Nisannu', 1, 'AG')
        assert bab.from_julian(45, 3, 10, 'seleucid') == (355, u"Addaru", 2, 'AG')

        assert bab.from_julian(45, 11, 30, 'seleucid') == (356, u"Kislimu", 1, 'AG')

        assert bab.from_julian(46, 2, 26, 'seleucid') == (356, u"Addaru", 1, 'AG')

    def test_prev_visible_nm(self):
        dc = dublin.from_gregorian(2014, 11, 25)
        self.assertEqual(bab.previous_visible_nm(dc).tuple(), (2014, 11, 22, 0, 0, 0))

    def test_babylon_from_jd_analeptic(self):
        self.assertEqual(bab.from_julian(46, 3, 27, 'seleucid'), (357, u'Nisannu', 1, 'AG'))

        self.assertEqual(bab.from_julian(100, 3, 2), (410, u'Addaru', 3, 'AG'))
        self.assertEqual(bab.from_julian(100, 4, 2), (411, u'Nisannu', 4, 'AG'))
        self.assertEqual(bab.from_julian(100, 5, 1), (411, u'Aiaru', 4, 'AG'))
        self.assertEqual(bab.from_julian(100, 6, 1), (411, u'Simanu', 5, 'AG'))

        for x in range(1757582, 1757582 + 100):
            bab.from_jd(x - 1, plain=1)
            self.compare_to_next(x)

        self.assertEqual(bab.from_gregorian(2014, 11, 7, plain=1), (2325, 'Arahsamnu', 15, 'AG'))

    def test_pd_analeptic_handoff(self):
        assert bab.from_julian(46, 2, 26) == (356, 'Addaru', 1, 'AG')
        assert bab.from_julian(46, 2, 28) == (356, 'Addaru', 3, 'AG')
        assert bab.from_julian(46, 3, 2) == (356, 'Addaru', 5, 'AG')
        assert bab.from_julian(46, 3, 4) == (356, 'Addaru', 7, 'AG')
        assert bab.from_julian(46, 3, 6) == (356, 'Addaru', 9, 'AG')
        assert bab.from_julian(46, 3, 8) == (356, 'Addaru', 11, 'AG')
        assert bab.from_julian(46, 3, 10) == (356, 'Addaru', 13, 'AG')
        assert bab.from_julian(46, 3, 12) == (356, 'Addaru', 15, 'AG')
        assert bab.from_julian(46, 3, 14) == (356, 'Addaru', 17, 'AG')
        assert bab.from_julian(46, 3, 16) == (356, 'Addaru', 19, 'AG')
        assert bab.from_julian(46, 3, 18) == (356, 'Addaru', 21, 'AG')
        assert bab.from_julian(46, 3, 20) == (356, 'Addaru', 23, 'AG')
        assert bab.from_julian(46, 3, 22) == (356, 'Addaru', 25, 'AG')
        assert bab.from_julian(46, 3, 24) == (356, 'Addaru', 27, 'AG')
        assert bab.from_julian(46, 3, 26) == (356, 'Addaru', 29, 'AG')
        assert bab.from_julian(46, 3, 28) == (357, 'Nisannu', 2, 'AG')

    def test_load_parker_dubberstein(self):
        bab.load_parker_dubberstein()
        parkerdub = bab.PARKER_DUBBERSTEIN

        assert parkerdub[-603].get('months')
        assert parkerdub[-580].get('months').get(6) == julian.to_jd(-580, 9, 12)

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

            try:
                self.assertGreater(diy, monlen * 29)
                self.assertLess(diy, monlen * 30)

            except AssertionError as e:
                print('****', pev)
                print(bab.intercalate(x))

                p = dublin.to_jd(pev.real)
                n = dublin.to_jd(nex.real)

                # Next year
                print(gregorian.from_jd(p), bab.from_jd(p))
                print(gregorian.from_jd(n), bab.from_jd(n))

                jd = int(p)

                for y in range(jd, jd + 730):
                    self.compare_to_next(y)

                raise e

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
        self.assertEqual(bab.to_julian(1, 1, 1, era='seleucid'), (-310, 4, 3))
        self.assertEqual(bab.to_julian(312, 1, 1, era='seleucid'), (1, 4, 14))
        assert bab.to_julian(311, 2, 3, era='seleucid') == (0, 4, 26)

        assert bab.to_julian(311, 12, 1, era='seleucid') == (1, 2, 14)
        assert bab.to_julian(311, 12, 5, era='seleucid') == (1, 2, 18)
        assert bab.to_julian(327, 1, 1, era='seleucid') == (16, 3, 29)

    def test_bab_to_julian_arsacid(self):
        self.assertEqual(bab.to_julian(1, 1, 1, era='arsacid'), (-246, 4, 15))
        assert bab.to_julian(2, 1, 1, era='arsacid') == (-245, 4, 4)
        assert bab.to_julian(22, 1, 1, era='arsacid') == (-225, 4, 22)
        assert bab.to_julian(232, 1, 1, era='arsacid') == (-15, 4, 11)
        assert bab.to_julian(142, 1, 1, era='arsacid') == (-105, 4, 17)
        assert bab.to_julian(242, 1, 1, era='arsacid') == (-5, 4, 20)
        assert bab.to_julian(263, 1, 1, era='arsacid') == (16, 3, 29)

    def test_bab_to_julian_regnal(self):
        self.assertRaises(ValueError, bab.to_julian, 1, 1, 1, era='regnal')
        self.assertEqual(bab.to_julian(1, 13, 1, era='regnal', ruler='Nabunaid'), (-553, 3, 20))
        assert bab.to_julian(1, 13, 10, era='regnal', ruler='Nabunaid') == (-553, 3, 29)

        assert bab.to_julian(3, 12, 1, era='regnal', ruler='Cyrus') == (-534, 2, 19)

        assert bab.to_julian(4, 13, 1, era='regnal', ruler='Nebuchadnezzar II') == (-599, 3, 18)

        assert bab.to_julian(0, 1, 1, era='regnal', ruler='Nabopolassar') == (-625, 4, 5)

        self.assertEqual(bab.to_julian(1, 1, 1, era='regnal', ruler='Nabopolassar'), (-624, 3, 24))
        self.assertEqual(bab.to_julian(0, 1, 1, era='regnal', ruler='Nabopolassar'), (-625, 4, 5))

        assert bab.to_julian(21, 10, 1, era='regnal', ruler='Nabopolassar') == (-603, 1, 3)

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

    #         print("{}\t{}\t{}\t{}".format(x, m, moon, v))
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

    def test_glitchy_1700s(self):
        for y in range(1691, 1691 + 19):
            ve = ephem.next_vernal_equinox(str(y) + '/1/1')
            nm = bab.next_visible_nm(ve)
            print("{}\t{}\t{}".format(ve, nm, round(nm - ve, 1)))

        for x in range(2342434 - 1, 2342434 + 5):
            self.compare_to_next(x)

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
            try:
                assert round(nvnm - pvnm, 0) in [29.0, 30.0, 29, 30, 30, 31.0]
            except AssertionError as e:
                print('test_overall_days_of_month', x, nvnm, pvnm)
                raise e

    def compare_to_next(self, jdn):
        one = bab.from_jd(jdn, plain=1)
        two = bab.from_jd(jdn + 1, plain=1)
        try:
            self.assertLessEqual(one[0], two[0])
            self.assertNotEqual(one, two)

            if one[2] not in [29, 30]:
                self.assertEqual(one[2] + 1, two[2])
            else:
                assert two[2] in [30, 1]
                if one[2] == 30:
                    self.assertNotEqual(one[1], two[1])

        except AssertionError as e:
            print('jd', jdn)
            print('one', one)
            print('two', two)
            raise e

    # def test_comparse_lunisolar(self):
    #     track_lunisolar_metonic(1900)
    #     track_lunisolar_metonic(45+19)

    def test_metonic_lag(self):
        for x in range(-518, 59 + (19 * 150), 19):
            ve = ephem.next_vernal_equinox(dublin.from_gregorian(bab.metonic_start(x), 1, 1))
            nmve = ephem.next_new_moon(ve)
            assert nmve - ve < 20


def compare_lunisolar_metonic(start):
    '''Compare the difference between the NM and VE at the end of the Metoinc Cycle'''
    start = bab.metonic_start(start)
    ve = ephem.next_vernal_equinox(dublin.from_gregorian(start, 1, 1))
    nm = ephem.next_new_moon(ve)
    for x in range(0, 19):
        ve = ephem.next_vernal_equinox(ve)

    for y in range(0, 235):
        nm = ephem.next_new_moon(nm)

    print("{}\t{}".format(start, round(nm - ve, 1)))


def track_lunisolar_metonic(inp):
    '''Compares start of bab year and NMVE for a metonic cycle'''
    start = bab.metonic_start(inp)
    ve = ephem.previous_vernal_equinox(dublin.from_gregorian(start, 6, 1))
    moon = ephem.previous_new_moon(ve)

    print('year\tMN\tVE\tnew moon\tdiff')

    for year in range(start, start + 19):
        print('*', ve)
        for x in range(1, 1 + len(bab.intercalate(year))):
            moon = ephem.next_new_moon(moon)
            print('**', x, moon)
            if x == 1:
                try:
                    assert moon > ve
                except AssertionError:
                    pass
                print('{}\t{}\t{}\t{}\t{}'.format(
                    year,
                    bab.metonic_number(year),
                    dublin.to_gregorian(ve.real),
                    dublin.to_gregorian(moon.real),
                    round(moon - ve, 1)
                ))

        ve = ephem.next_vernal_equinox(ve)


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
