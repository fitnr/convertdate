# -*- coding: utf-8 -*-
import unittest
import time
import pytz
from datetime import datetime
from convertdate import utils
from convertdate import bahai
from convertdate import dublin
from convertdate import gregorian
from convertdate import hebrew
from convertdate import islamic
from convertdate import indian_civil
from convertdate import iso
from convertdate import julian
from convertdate import julianday
from convertdate import persian
from convertdate import ordinal


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
        self.assertEqual(utils.amod(100, 4), 4)
        self.assertEqual(utils.ceil(1.2), 2)
        self.assertEqual(utils.jwday(self.jd), self.tm[6])

    def reflexive(self, from_func, to_func):
        for jd in self.jdcs:
            self.assertEqual(jd + 0.5, to_func(*from_func(jd + 0.5)))

    def test_julian_legal_date(self):
        try:
            julian.to_jd(1900, 2, 29)
        except IndexError:
            self.fail('Unexpected IndexError: "julian.to_jd(1900, 2, 29)"')

        self.assertRaises(IndexError, julian.to_jd, 2014, 2, 29)
        self.assertRaises(IndexError, julian.to_jd, 2014, 3, 32)
        self.assertRaises(IndexError, julian.to_jd, 2014, 4, 31)
        self.assertRaises(IndexError, julian.to_jd, 2014, 5, -1)

    def test_hebrew(self):
        self.assertEqual(self.jd, hebrew.to_jd(*hebrew.from_jd(self.jd)))
        self.reflexive(hebrew.from_jd, hebrew.to_jd)

    def test_islamic(self):
        self.assertEqual(self.jd, islamic.to_jd(*islamic.from_jd(self.jd)))
        self.reflexive(islamic.from_jd, islamic.to_jd)

    def test_persian(self):
        self.assertEqual(self.jd, persian.to_jd(*persian.from_jd(self.jd)))

        self.assertEqual(persian.leap(-101), False)

        self.reflexive(persian.from_jd, persian.to_jd)

    def test_indian_civil(self):
        self.assertEqual(self.jd, indian_civil.to_jd(*indian_civil.from_jd(self.jd)))
        self.reflexive(indian_civil.from_jd, indian_civil.to_jd)

    def test_iso(self):
        self.assertEqual(iso.from_gregorian(2005, 1, 1), (2004, 53, 6))
        self.assertEqual(iso.to_gregorian(2004, 53, 6), (2005, 1, 1))

        self.assertEqual(self.jd, iso.to_jd(*iso.from_jd(self.jd)))
        self.reflexive(iso.from_jd, iso.to_jd)

    def test_ordinal(self):
        self.assertEqual(ordinal.from_gregorian(2013, 1, 1), (2013, 1))
        self.assertEqual(ordinal.from_gregorian(2013, 2, 1), (2013, 32))
        self.assertEqual(ordinal.from_gregorian(2013, 3, 1), (2013, 60))
        self.assertEqual(ordinal.from_gregorian(2013, 4, 15), (2013, 105))

        self.reflexive(ordinal.from_jd, ordinal.to_jd)

    def test_ordinal_to_gregorian(self):
        self.assertEqual(ordinal.to_gregorian(2013, 1), (2013, 1, 1))
        self.assertEqual(ordinal.to_gregorian(2013, 105), (2013, 4, 15))
        self.assertEqual(ordinal.to_gregorian(2013, 32), (2013, 2, 1))
        self.assertEqual(ordinal.to_gregorian(2012, 1), (2012, 1, 1))
        self.assertEqual(ordinal.to_gregorian(2012, 31), (2012, 1, 31))
        self.assertEqual(ordinal.to_gregorian(2012, 32), (2012, 2, 1))
        self.assertEqual(ordinal.to_gregorian(2012, 52), (2012, 2, 21))
        self.assertEqual(ordinal.to_gregorian(2012, 59), (2012, 2, 28))
        self.assertEqual(ordinal.to_gregorian(2012, 60), (2012, 2, 29))
        self.assertEqual(ordinal.to_gregorian(2012, 61), (2012, 3, 1))

    def test_from_julian(self):
        self.assertEqual(self.jd, julian.to_jd(*julian.from_jd(self.jd)))
        self.assertEqual(julian.from_jd(self.c), (1492, 10, 12))
        self.assertEqual(julian.from_jd(2400000.5), (1858, 11, 5))
        self.assertEqual(julian.from_jd(2399830.5), (1858, 5, 19))

    def test_julian_inverse(self):
        self.reflexive(julian.from_jd, julian.to_jd)

    def test_to_julian(self):
        self.assertEqual(julian.to_jd(1858, 11, 5), 2400000.5)
        self.assertEqual(julian.to_jd(1492, 10, 12), self.c)

    def test_bahai(self):
        self.reflexive(bahai.from_jd, bahai.to_jd)

        self.assertEqual(bahai.from_gregorian(1844, 3, 21), (1, 1, 1))
        self.assertEqual(bahai.to_gregorian(1, 1, 1), (1844, 3, 21))

        self.assertEqual(bahai.month_length(1, 3), 19)
        self.assertEqual(bahai.month_length(1, 1), 19)
        self.assertEqual(bahai.month_length(4, 19), 5)
        self.assertEqual(bahai.month_length(5, 19), 4)

        self.assertEqual(self.jd, bahai.to_jd(*bahai.from_jd(self.jd)))

    def test_dublin_dc(self):
        self.assertEqual(dublin.from_gregorian(1900, 1, 1), 0.5)
        self.assertEqual(dublin.to_gregorian(1), (1900, 1, 1))
        self.assertEqual(dublin.to_jd(0), 2415020.0)

        self.assertEqual(
            dublin.to_jd(dublin.from_jd(self.c)),
            gregorian.to_jd(*dublin.to_gregorian(dublin.from_gregorian(*self.c_greg)))
        )

        self.assertEqual(dublin.to_gregorian(dublin.from_jd(1737936)), gregorian.from_jd(1737936))
        self.assertEqual(dublin.to_julian(dublin.from_jd(1737936)), julian.from_jd(1737936))

    def test_julian_day(self):
        self.assertEqual(julianday.from_gregorian(*self.c_greg), self.c)
        self.assertEqual(julianday.to_datetime(self.c), datetime(1492, 10, 21, tzinfo=pytz.utc))
        self.assertEqual(julianday.to_datetime(self.x), datetime(2016, 2, 29, tzinfo=pytz.utc))

        self.assertEqual(julianday.to_datetime(self.c + 0.25), datetime(1492, 10, 21, 6, tzinfo=pytz.utc))
        self.assertEqual(julianday.to_datetime(self.x + 0.525), datetime(2016, 2, 29, 12, 36, tzinfo=pytz.utc))

        dt = datetime(2014, 11, 8, 3, 37, tzinfo=pytz.utc)
        self.assertEqual(julianday.from_datetime(dt), 2456969.65069)

        self.assertEqual(julianday.to_datetime(self.x + 0.525), datetime(2016, 2, 29, 12, 36, tzinfo=pytz.utc))

    def test_month_length_indian_civil(self):
        self.assertEqual(indian_civil.month_length(1922, 1), 31)
        self.assertEqual(indian_civil.month_length(1923, 1), 30)

    def test_month_length_julian(self):
        self.assertEqual(julian.month_length(1582, 10), 31)
        self.assertEqual(julian.month_length(1977, 2), 28)
        self.assertEqual(julian.month_length(1900, 2), 29)
        self.assertEqual(julian.month_length(1904, 2), 29)

    def test_month_length_islamic(self):
        self.assertEqual(islamic.month_length(1436, 1), 30)
        self.assertEqual(islamic.month_length(1436, 2), 29)
        self.assertEqual(islamic.month_length(1436, 12), 30)

    def test_month_length_persian(self):
        self.assertEqual(persian.month_length(1354, 12), 30)
        self.assertEqual(persian.month_length(1355, 12), 29)

    def test_monthcalendar_indian_civil(self):
        self.assertEqual(indian_civil.monthcalendar(1936, 8).pop(0).pop(4), 1)
        self.assertEqual(indian_civil.monthcalendar(1927, 2).pop(0).pop(4), 1)
        self.assertEqual(indian_civil.monthcalendar(1922, 1).pop().pop(4), 31)

    def test_monthcalendar_julian(self):
        self.assertEqual(julian.monthcalendar(1582, 10).pop(0).pop(1), 1)
        self.assertEqual(julian.monthcalendar(1582, 10).pop().pop(3), 31)

    def test_monthcalendar_islamic(self):
        self.assertEqual(islamic.monthcalendar(1436, 10).pop(0).pop(6), 1)
        self.assertEqual(islamic.monthcalendar(1436, 11).pop().pop(1), 30)

    def test_monthcalendar_persian(self):
        self.assertEqual(persian.monthcalendar(1393, 8).pop(0).pop(4), 1)
        self.assertEqual(persian.monthcalendar(1393, 8).pop().pop(0), 25)

    def test_monthcalendar_hebrew(self):
        self.assertEqual(hebrew.monthcalendar(5775, 7).pop(0).pop(4), 1)
        self.assertEqual(hebrew.monthcalendar(5775, 7).pop().pop(0), 25)


if __name__ == '__main__':
    unittest.main()
