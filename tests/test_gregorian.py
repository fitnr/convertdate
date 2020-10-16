# -*- coding: utf-8 -*-
import time

from convertdate import gregorian, julian

from . import CalTestCase


class TestGregorian(CalTestCase):
    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

        self.c_greg = (1492, 10, 21)
        self.c = gregorian.to_jd(*self.c_greg)

        self.jdcs = range(2159677, 2488395, 2000)

    def test_gregorian(self):
        assert gregorian.to_jd(*self.gregoriandate) == self.jd
        assert gregorian.to_jd2(*self.gregoriandate) == self.jd

        self.assertEqual(self.c, 2266295.5)
        assert gregorian.to_jd(2000, 1, 1) == 2451544.5

        assert gregorian.to_jd2(2000, 1, 1) == 2451544.5

        self.reflexive(gregorian)

    def test_gregorian_proleptic(self):
        self.assertEqual(gregorian.to_jd(72, 6, 27), 1747535.5)
        assert gregorian.to_jd2(72, 6, 27) == 1747535.5

        for y in range(int(gregorian.EPOCH), int(gregorian.EPOCH) - 10000, -250):
            assert gregorian.to_jd(*gregorian.from_jd(y)) == y - 0.5

        assert gregorian.from_jd(gregorian.to_jd(-1, 3, 1)) == (-1, 3, 1)
        assert gregorian.from_jd(gregorian.to_jd(-100, 7, 1)) == (-100, 7, 1)
        assert gregorian.from_jd(gregorian.to_jd(-500, 12, 31)) == (-500, 12, 31)
        assert gregorian.from_jd(gregorian.to_jd(-1000, 1, 1)) == (-1000, 1, 1)

    def test_from_gregorian_20thc(self):
        self.assertEqual(gregorian.from_jd(2418934.0), (1910, 9, 19))
        self.assertEqual(gregorian.from_jd(2433360.0), (1950, 3, 19))
        self.assertEqual(gregorian.from_jd(2437970.0), (1962, 11, 1))
        self.assertEqual(gregorian.from_jd(2447970.0), (1990, 3, 19))
        self.assertEqual(gregorian.from_jd(2456967.5), (2014, 11, 6))

    def test_to_gregorian(self):
        self.assertEqual(gregorian.to_jd(2014, 11, 5), 2456966.5)

        assert gregorian.to_jd(2012, 3, 1) == 1 + gregorian.to_jd(2012, 2, 29)

        assert gregorian.from_jd(gregorian.to_jd(2012, 2, 29) + 1) == (2012, 3, 1)
        assert gregorian.from_jd(gregorian.to_jd(2011, 2, 28) + 1) == (2011, 3, 1)

        assert gregorian.from_jd(gregorian.to_jd(2012, 3, 2) - 2) == (2012, 2, 29)
        assert gregorian.from_jd(gregorian.to_jd(2011, 3, 2) - 2) == (2011, 2, 28)

    def test_gregorian_1_ma(self):
        assert gregorian.to_jd(*self.c_greg) == 2266295.5

    def test_gregorian_2_ma(self):
        assert gregorian.to_jd2(*self.c_greg) == 2266295.5

    def test_gregorian_julian_dif_proleptic(self):
        self.assertEqual(julian.to_jd(1500, 5, 10), gregorian.to_jd(1500, 5, 20))
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
        self.assertEqual(gregorian.from_jd(gregorian.to_jd(1, 1, 1) - 1), (0, 12, 31))

    def test_legal_date(self):
        self.assertRaises(ValueError, gregorian.to_jd, 1900, 2, 29)
        self.assertRaises(ValueError, gregorian.to_jd, 2014, 2, 29)
        self.assertRaises(ValueError, gregorian.to_jd, 2014, 3, 32)
        self.assertRaises(ValueError, gregorian.to_jd, 2014, 4, 31)
        self.assertRaises(ValueError, gregorian.to_jd, 2014, 5, -1)
