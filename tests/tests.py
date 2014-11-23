# -*- coding: utf-8 -*-
"python -m unittest convertdate.tests"

import unittest
import time
import pytz
from datetime import datetime
from convertdate import utils
from convertdate import bahai
from convertdate import french_republican as fr
from convertdate import dublin
from convertdate import gregorian
from convertdate import hebrew
from convertdate import islamic
from convertdate import indian_civil
from convertdate import iso
from convertdate import julian
from convertdate import julianday
from convertdate import mayan
from convertdate import persian

from convertdate import holidays


class CalTestCase(unittest.TestCase):

    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

        self.c_greg = (1492, 10, 21)
        self.c = gregorian.to_jd(*self.c_greg)
        self.x = gregorian.to_jd(2016, 2, 29)

        self.jdcs = range(2159677, 2488395, 2000)

    def test_utils(self):
        assert utils.amod(100, 4) == 4
        assert utils.ceil(1.2) == 2
        assert utils.jwday(self.jd) == self.tm[6]

    def reflexive(self, from_func, to_func):
        for jd in self.jdcs:
            self.assertEqual(jd + 0.5, to_func(*from_func(jd + 0.5)))

    def test_gregorian(self):
        assert gregorian.to_jd(*self.gregoriandate) == self.jd
        assert gregorian.to_jd2(*self.gregoriandate) == self.jd

        assert self.c == 2266295.5
        assert gregorian.to_jd(2000, 1, 1) == 2451544.5

        assert gregorian.to_jd2(2000, 1, 1) == 2451544.5

        self.reflexive(gregorian.from_jd, gregorian.to_jd)

    def test_gregorian_proleptic(self):
        assert gregorian.to_jd(72, 6, 27) == 1747535.5
        assert gregorian.to_jd2(72, 6, 27) == 1747535.5

        for y in range(int(gregorian.EPOCH), int(gregorian.EPOCH) - 10000, -250):
            assert gregorian.to_jd(*gregorian.from_jd(y)) == y - 0.5

        assert gregorian.from_jd(gregorian.to_jd(-1, 3, 1)) == (-1, 3, 1)
        assert gregorian.from_jd(gregorian.to_jd(-100, 7, 1)) == (-100, 7, 1)
        assert gregorian.from_jd(gregorian.to_jd(-500, 12, 31)) == (-500, 12, 31)
        assert gregorian.from_jd(gregorian.to_jd(-1000, 1, 1)) == (-1000, 1, 1)

    def test_gregorian_1_ma(self):
        assert gregorian.to_jd(*self.c_greg) == 2266295.5

    def test_gregorian_2_ma(self):
        assert gregorian.to_jd2(*self.c_greg) == 2266295.5

    def test_gregorian_julian_dif_proleptic(self):
        assert julian.to_jd(1500, 5, 10) == gregorian.to_jd(1500, 5, 20)
        assert julian.to_jd(1300, 5, 10) == gregorian.to_jd(1300, 5, 18)
        assert julian.to_jd(1000, 5, 10) == gregorian.to_jd(1000, 5, 16)
        assert julian.to_jd(900, 5, 10) == gregorian.to_jd(900, 5, 15)
        assert julian.to_jd(300, 5, 10) == gregorian.to_jd(300, 5, 11)
        assert julian.to_jd(200, 5, 10) == gregorian.to_jd(200, 5, 10)
        assert julian.to_jd(100, 5, 10) == gregorian.to_jd(100, 5, 9)
        assert julian.to_jd(-1, 5, 10) == gregorian.to_jd(-1, 5, 8)

    def test_year_zero(self):
        assert gregorian.to_jd(1, 1, 1) == 1.0 + gregorian.to_jd(0, 12, 31)
        assert julian.to_jd(1, 1, 1) == 1.0 + julian.to_jd(0, 12, 31)

        assert julian.from_jd(julian.to_jd(1, 1, 1) - 1) == (0, 12, 31)
        assert gregorian.from_jd(gregorian.to_jd(1, 1, 1) - 1) == (0, 12, 31)

    def test_legal_date(self):
        self.assertRaises(IndexError, gregorian.to_jd, 1900, 2, 29)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 2, 29)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 3, 32)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 4, 31)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 5, -1)

        try:
            julian.to_jd(1900, 2, 29)
        except IndexError:
            self.fail('Unexpected IndexError: "julian.to_jd(1900, 2, 29)"')

        self.assertRaises(IndexError, julian.to_jd, 2014, 2, 29)
        self.assertRaises(IndexError, julian.to_jd, 2014, 3, 32)
        self.assertRaises(IndexError, julian.to_jd, 2014, 4, 31)
        self.assertRaises(IndexError, julian.to_jd, 2014, 5, -1)

    def test_mayan_reflexive(self):
        assert self.jd == mayan.to_jd(*mayan.from_jd(self.jd))

        self.reflexive(mayan.from_jd, mayan.to_jd)

    def test_mayan_count(self):
        assert mayan.to_jd(13, 0, 0, 0, 0) == 2456282.5
        assert mayan.from_gregorian(2012, 12, 21) == (13, 0, 0, 0, 0)
        assert mayan.to_gregorian(13, 0, 0, 0, 0) == (2012, 12, 21)
        assert mayan.from_jd(self.c) == (11, 13, 12, 4, 13)

    def test_mayan_haab(self):
        # haab
        assert mayan.HAAB_MONTHS[2] == 'Zip'
        assert mayan.HAAB_MONTHS.index("Xul") == 5
        assert mayan.to_haab(self.c) == (16, "Sotz'")
        assert mayan.to_haab(2456282.5) == (3, "K'ank'in")

    def test_mayan_tzolkin(self):
        # tzolkin
        assert mayan.TZOLKIN_NAMES[0] == "Imix'"
        assert mayan.to_tzolkin(self.c) == (12, "B'en")
        assert mayan.to_tzolkin(2456282.5) == (4, 'Ajaw')
        assert mayan.to_tzolkin(2456850.5) == (13, 'Lamat')

    def test_mayan_convenience(self):

        assert mayan.lc_to_haab(0, 0, 0, 0, 0) == (8, "Kumk'u")
        assert mayan.lc_to_tzolkin(0, 0, 0, 0, 0) == (4, "Ajaw")

        assert mayan.lc_to_tzolkin(9, 16, 12, 5, 17) == (6, "Kab'an")
        assert mayan.lc_to_haab(9, 16, 12, 5, 17) == (10, "Mol")

        assert mayan.lc_to_haab_tzolkin(9, 16, 12, 5, 17) == "6 Kab'an 10 Mol"

        assert mayan.translate_haab("Wayeb'") == 'Nameless'

    def test_mayan_predictions(self):
        assert mayan.next_haab("Sotz'", self.c) == 2266280.5

        for h in mayan.HAAB_MONTHS:
            assert mayan.to_haab(mayan.next_haab(h, self.c)) == (1, h)

        assert mayan.next_tzolkin_haab((13, "Ajaw"), (3, "Kumk'u"), 2456849.5) == 2463662.5

    def test_french_republican(self):
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd))

        assert fr.from_gregorian(2014, 6, 14) == (222, 9, 26)

        self.assertEqual(gregorian.to_jd(1793, 9, 22), fr.to_jd(2, 1, 1))

        # 9 Thermidor II
        self.assertEqual(gregorian.to_jd(1794, 7, 27), fr.to_jd(2, 11, 9))

        for jd in range(2378822, 2488395, 2000):
            self.assertEqual(jd + 0.5, gregorian.to_jd(*gregorian.from_jd(jd + 0.5)))

    def test_french_republican_schematic(self):
        self.assertRaises(ValueError, fr.from_jd, self.jd, method=400)

        assert self.jd == fr.to_jd(*fr.from_jd(self.jd, method=128), method=128)
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd, method=100), method=100)
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd, method=4), method=4)

        j = self.jd - 265 * 150
        assert j == fr.to_jd(*fr.from_jd(j, method=128), method=128)
        assert j == fr.to_jd(*fr.from_jd(j, method=100), method=100)
        assert j == fr.to_jd(*fr.from_jd(j, method=4), method=4)

    def test_french_republican_names(self):
        self.assertEqual(fr.day_name(1, 1), u"Raisin")
        assert fr.day_name(2, 1) == u"Pomme"
        assert fr.day_name(4, 18) == u"Pierre à chaux"
        assert fr.day_name(12, 15) == u"Truite"
        assert fr.day_name(13, 1) == u"La Fête de la Vertu"

    def test_hebrew(self):
        self.assertEqual(self.jd, hebrew.to_jd(*hebrew.from_jd(self.jd)))

        self.reflexive(hebrew.from_jd, hebrew.to_jd)

    def test_islamic(self):
        assert self.jd == islamic.to_jd(*islamic.from_jd(self.jd))

        self.reflexive(islamic.from_jd, islamic.to_jd)

    def test_persian(self):
        assert self.jd == persian.to_jd(*persian.from_jd(self.jd))

        self.reflexive(persian.from_jd, persian.to_jd)

    def test_indian_civil(self):
        assert self.jd == indian_civil.to_jd(*indian_civil.from_jd(self.jd))
        self.reflexive(indian_civil.from_jd, indian_civil.to_jd)

    def test_iso(self):
        assert self.jd == iso.to_jd(*iso.from_jd(self.jd))

        self.reflexive(iso.from_jd, iso.to_jd)

    def test_from_julian(self):
        assert self.jd == julian.to_jd(*julian.from_jd(self.jd))
        assert julian.from_jd(self.c) == (1492, 10, 12)
        assert julian.from_jd(2400000.5) == (1858, 11, 5)
        assert julian.from_jd(2399830.5) == (1858, 5, 19)

    def test_from_gregorian_20thc(self):
        assert gregorian.from_jd(2418934.0) == (1910, 9, 19)
        assert gregorian.from_jd(2433360.0) == (1950, 3, 19)
        assert gregorian.from_jd(2437970.0) == (1962, 11, 1)
        assert gregorian.from_jd(2447970.0) == (1990, 3, 19)
        assert gregorian.from_jd(2456967.5) == (2014, 11, 6)

    def test_to_gregorian(self):
        assert gregorian.to_jd(2014, 11, 5) == 2456966.5

    def test_julian_inverse(self):
        self.reflexive(julian.from_jd, julian.to_jd)

    def test_to_julian(self):
        assert julian.to_jd(1858, 11, 5) == 2400000.5
        assert julian.to_jd(1492, 10, 12) == self.c

    def test_bahai(self):
        self.reflexive(bahai.from_jd, bahai.to_jd)

        self.assertEqual(bahai.from_gregorian(1844, 3, 20), (1, 1, 1))
        self.assertEqual(bahai.to_gregorian(1, 1, 1), (1844, 3, 20))

        assert self.jd == bahai.to_jd(*bahai.from_jd(self.jd))

    def test_holidays(self):
        h = holidays.Holidays(2014)
        assert h.christmas == (2014, 12, 25)
        assert h.thanksgiving == (2014, 11, 27)
        assert h.columbus_day == (2014, 10, 13)

    def test_thanksgiving(self):
        assert holidays.thanksgiving(2013) == (2013, 11, 28)
        assert holidays.thanksgiving(1939) == (1939, 11, 23)
        assert holidays.thanksgiving(1941) == (1941, 11, 20)

    def test_easter(self):
        easters = [
            (1994, 4, 3),
            (1995, 4, 16),
            (1996, 4, 7),
            (1997, 3, 30),
            (1998, 4, 12),
            (1999, 4, 4),
            (2000, 4, 23),
            (2001, 4, 15),
            (2002, 3, 31),
            (2003, 4, 20),
            (2004, 4, 11),
            (2005, 3, 27),
            (2006, 4, 16),
            (2007, 4, 8),
            (2008, 3, 23),
            (2009, 4, 12),
            (2010, 4, 4),
            (2011, 4, 24),
            (2012, 4, 8),
            (2013, 3, 31),
            (2014, 4, 20),
            (2015, 4, 5),
            (2016, 3, 27),
            (2017, 4, 16),
            (2018, 4, 1),
            (2019, 4, 21),
            (2020, 4, 12),
            (2021, 4, 4),
            (2022, 4, 17),
            (2023, 4, 9),
            (2024, 3, 31),
            (2025, 4, 20),
            (2026, 4, 5),
            (2027, 3, 28),
            (2028, 4, 16),
            (2029, 4, 1),
            (2030, 4, 21),
            (2031, 4, 13),
            (2032, 3, 28),
            (2033, 4, 17),
            (2034, 4, 9)
        ]
        for y, m, d in easters:
            self.assertEqual(holidays.easter(y), (y, m, d))

    def test_jewish_holidays(self):
        # http://www.chabad.org/holidays/passover/pesach_cdo/aid/671901/jewish/When-is-Passover-in-2013-2014-2015-2016-and-2017.htm
        # the date here is the start of the holiday, so the eve=1 option is used
        passovers = [
            (2013, 3, 25),
            (2014, 4, 14),
            (2015, 4, 3),
            (2016, 4, 22),
            (2017, 4, 10)
        ]
        for y, m, d in passovers:
            self.assertEqual(holidays.passover(y, eve=1), (y, m, d))

        rosh_hashanahs = [
            (2014, 9, 24),
            (2015, 9, 13),
            (2016, 10, 2),
            (2017, 9, 20),
        ]
        for y, m, d in rosh_hashanahs:
            self.assertEqual(holidays.rosh_hashanah(y, eve=1), (y, m, d))

    def test_nth_day_of_month(self):
        assert holidays.nth_day_of_month(4, 2, 4, 2014) == (2014, 4, 23)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 5, 3, 4, 2014)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 6, 2, 4, 2014)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 1, 7, 4, 2014)
        assert holidays.nth_day_of_month(4, 3, 11, 2014) == (2014, 11, 27)
        assert holidays.nth_day_of_month(0, 3, 11, 2014) == (2014, 11, 27)

    def test_dublin_dc(self):
        assert dublin.from_gregorian(1900, 1, 1) == 0.5
        assert dublin.to_gregorian(1) == (1900, 1, 1)
        assert dublin.to_jd(0) == 2415020.0

        assert dublin.to_jd(dublin.from_jd(self.c)) == gregorian.to_jd(*dublin.to_gregorian(dublin.from_gregorian(*self.c_greg)))

        assert dublin.to_gregorian(dublin.from_jd(1737936)) == gregorian.from_jd(1737936)
        assert dublin.to_julian(dublin.from_jd(1737936)) == julian.from_jd(1737936)

    def test_julian_day(self):
        assert julianday.from_gregorian(*self.c_greg) == self.c
        assert julianday.to_datetime(self.c) == datetime(1492, 10, 21, tzinfo=pytz.utc)
        assert julianday.to_datetime(self.x) == datetime(2016, 2, 29, tzinfo=pytz.utc)

        assert julianday.to_datetime(self.c + 0.25) == datetime(1492, 10, 21, 6, tzinfo=pytz.utc)
        assert julianday.to_datetime(self.x + 0.525) == datetime(2016, 2, 29, 12, 36, tzinfo=pytz.utc)

        dt = datetime(2014, 11, 8, 3, 37, tzinfo=pytz.utc)
        assert julianday.from_datetime(dt) == 2456969.65069

        assert julianday.to_datetime(self.x + 0.525) == datetime(2016, 2, 29, 12, 36, tzinfo=pytz.utc)

    def test_month_length(self):
        assert indian_civil.month_length(1922, 1) == 31
        assert indian_civil.month_length(1923, 1) == 30

        assert julian.month_length(1582, 10) == 31
        assert julian.month_length(1977, 2) == 28
        assert julian.month_length(1900, 2) == 29
        assert julian.month_length(1904, 2) == 29

        assert islamic.month_length(1436, 1) == 30
        assert islamic.month_length(1436, 2) == 29
        assert islamic.month_length(1436, 12) == 30

        assert persian.month_length(1354, 12) == 30
        assert persian.month_length(1355, 12) == 29

    def test_monthcalendar(self):
        assert indian_civil.monthcalendar(1936, 8).pop(0).pop(4) == 1
        assert indian_civil.monthcalendar(1927, 2).pop(0).pop(4) == 1
        assert indian_civil.monthcalendar(1922, 1).pop().pop(4) == 31

        assert julian.monthcalendar(1582, 10).pop(0).pop(1) == 1
        assert julian.monthcalendar(1582, 10).pop().pop(3) == 31

        assert islamic.monthcalendar(1436, 10).pop(0).pop(6) == 1
        assert islamic.monthcalendar(1436, 11).pop().pop(1) == 30

        assert persian.monthcalendar(1393, 8).pop(0).pop(4) == 1
        assert persian.monthcalendar(1393, 8).pop().pop(0) == 25

        assert hebrew.monthcalendar(5775, 7).pop(0).pop(4) == 1
        assert hebrew.monthcalendar(5775, 7).pop().pop(0) == 25

    def test_mayan_monthcalendar(self):
        calendar = mayan.haab_monthcalendar(13, 0, 2, 11, 13)
        row = calendar[0]
        square = row[-1]
        assert type(row) == list
        assert type(square) == tuple
        assert row[7][0] == 1

        assert mayan.to_jd(*calendar[-1][-1][-1]) == 19 + mayan.to_jd(13, 0, 2, 11, 13)
        assert square == (6, (13, "Etz'nab'"), (13, 0, 2, 11, 18))

    def test_mayan_generators(self):
        lcg = mayan.longcount_generator(13, 0, 2, 11, 13)
        assert next(lcg) == (13, 0, 2, 11, 13)
        assert next(lcg) == (13, 0, 2, 11, 14)
        assert next(lcg) == (13, 0, 2, 11, 15)

        tzg = mayan.tzolkin_generator(9, "Ix")
        self.assertEqual(next(tzg), (9, "Ix"))
        assert next(tzg) == (10, "Men")
        assert next(tzg) == (11, "K'ib'")

if __name__ == '__main__':
    unittest.main()
