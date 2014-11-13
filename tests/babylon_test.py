# -*- coding: utf-8 -*-
from copy import copy
import unittest
from convertdate import dublin
from convertdate import julian
from convertdate import babylonian as bab
from convertdate.data import babylonian_data as data
import ephem


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
        assert bab.intercalation(1) == dict(zip(range(1, 13), data.MONTHS))

        leapyear_A = bab.intercalate(-385)
        assert len(leapyear_A) == 13
        assert leapyear_A[13] == u"Addaru II"

        assert len(bab.intercalate(-576)) == 12
        assert len(bab.intercalate(-595)) == 12
        assert len(bab.intercalate(-535)) == 12

        leapyear_U = bab.intercalate(-596)

        assert bab.intercalation_pattern('U') == {
            1: u'Nisannu', 2: u'Aiaru', 3: u'Simanu', 4: u'Duzu', 5: u'Abu', 6: u'Ululu',
            7: u'Ululu II', 8: u'Tashritu', 9: u'Araḥsamnu', 10: u'Kislimu', 11: u'Ṭebetu',
            12: u'Shabaṭu', 13: u'Addaru'}

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
        assert bab.previous_visible_nm(dc).tuple() == (2014, 11, 23, 13, 58, 27.14136839378625)

    def test_babylon_from_jd_analeptic(self):
        assert bab.from_julian(46, 3, 27, 'seleucid') == (357, u'Addaru II', 30)

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

        assert bab.from_julian(100, 3, 2) == (410, u'Addaru', 3)
        assert bab.from_julian(100, 4, 2) == (411, u'Nisannu', 4)
        assert bab.from_julian(100, 5, 2) == (411, u'Aiaru', 4)
        assert bab.from_julian(100, 6, 2) == (411, u'Simanu', 6)

        assert bab.from_gregorian(2014, 11, 7, plain=1) == (2325, 'Arahsamnu', 14)

    def test_load_parker_dubberstein(self):
        bab.load_parker_dubberstein()
        parkerdub = bab.PARKER_DUBBERSTEIN

        assert parkerdub[-604].get('months')
        assert parkerdub[-581].get('months').get(6) == julian.to_jd(-581, 9, 12)

        # print '\nyear\tmonth\tday\tM\tpve\tnm\n'
        # for x in range(-626, -311):
        #     try:
        #         start_o_year = parkerdub[x]['months'][1]
        #         thing(start_o_year)
        #     except KeyError:
        #         pass

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


def thing(jdc):
    dc = dublin.from_jd(jdc)
    pve = ephem.previous_vernal_equinox(dc)
    days_since_pve = dc - pve
    days_since_nm = dc - ephem.previous_new_moon(dc)
    jy, jm, jd = julian.from_jd(jdc)

    print "{year}\t{month}\t{day}\t{M}\t{pve}\t{nm}".format(
        year=jy, month=jm, day=jd,
        pve=int(days_since_pve),
        nm=int(days_since_nm),
        M=bab.metonic_number(jy)
    )


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

    for months in metonic.values():
        metonic_months.append(len(months))

    return metonic_months


if __name__ == '__main__':
    unittest.main()
