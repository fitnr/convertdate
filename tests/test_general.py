# -*- coding: utf-8 -*-
import time
from datetime import datetime, timezone

from convertdate import coptic, dublin, gregorian, hebrew, islamic, iso, julian, julianday, ordinal, persian, utils

from . import CalTestCase


class TestConvertdate(CalTestCase):
    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

        self.c_greg = (1492, 10, 21)
        self.c = gregorian.to_jd(*self.c_greg)
        self.x = gregorian.to_jd(2016, 2, 29)

        self.jdcs = range(2159677, 2488395, 2000)

    def test_julian_legal_date(self):
        try:
            julian.to_jd(1900, 2, 29)
        except ValueError:
            self.fail('Unexpected ValueError: "julian.to_jd(1900, 2, 29)"')

        self.assertRaises(ValueError, julian.to_jd, 2014, 2, 29)
        self.assertRaises(ValueError, julian.to_jd, 2014, 3, 32)
        self.assertRaises(ValueError, julian.to_jd, 2014, 4, 31)
        self.assertRaises(ValueError, julian.to_jd, 2014, 5, -1)

    def test_hebrew(self):
        self.assertEqual(self.jd, hebrew.to_jd(*hebrew.from_jd(self.jd)))
        self.reflexive(hebrew)

        # Anno Mundi
        am = hebrew.to_jd(1, hebrew.TISHRI, 1)
        self.assertEqual(julian.from_jd(am), (-3760, 10, 7))

    def test_islamic(self):
        self.assertEqual(self.jd, islamic.to_jd(*islamic.from_jd(self.jd)))
        self.reflexive(islamic)

        new_years = [
            (2012, 11, 15),
            (2015, 10, 15),
            (2019, 9, 1),
            (2020, 8, 20),
            (2021, 8, 10),
            (2022, 7, 30),
        ]

        for date in new_years:
            jd = islamic.to_jd_gregorianyear(date[0], 1, 1)
            with self.subTest(date[0]):
                self.assertEqual(date, gregorian.from_jd(jd))

        self.assertEqual(islamic.from_jd(1948085.5), (0, 1, 1))
        self.assertEqual(islamic.from_jd(1948084.5), (-1, 12, 30))
        self.assertEqual(islamic.from_jd(1912648.5), (-100, 1, 1))
        self.assertEqual(islamic.to_jd(-100, 1, 1), 1912648.5)

    def test_iso(self):
        self.assertEqual(iso.from_gregorian(2005, 1, 1), (2004, 53, 6))
        self.assertEqual(iso.to_gregorian(2004, 53, 6), (2005, 1, 1))

        self.assertEqual(self.jd, iso.to_jd(*iso.from_jd(self.jd)))
        self.reflexive(iso)

    def test_from_julian(self):
        self.assertEqual(self.jd, julian.to_jd(*julian.from_jd(self.jd)))
        self.assertEqual(julian.from_jd(self.c), (1492, 10, 12))
        self.assertEqual(julian.from_jd(2400000.5), (1858, 11, 5))
        self.assertEqual(julian.from_jd(2399830.5), (1858, 5, 19))

    def test_julian_inverse(self):
        self.reflexive(julian)

    def test_to_julian(self):
        self.assertEqual(julian.to_jd(1858, 11, 5), 2400000.5)
        self.assertEqual(julian.to_jd(1492, 10, 12), self.c)

    def test_coptic(self):
        self.assertEqual(coptic.to_jd(1000, 1, 1), 2189914.5)
        self.assertEqual(coptic.to_jd(1666, 6, 1), 2433320.5)
        self.assertEqual(coptic.to_jd(1, 1, 1), 1825029.5)
        self.assertEqual(coptic.from_jd(2437970.5), (1679, 2, 23))
        self.assertEqual(coptic.to_jd(1259, 13, 6), 2284878.5)
        self.assertEqual(coptic.from_jd(2284878.5), (1259, 13, 6))
        self.reflexive(coptic)
        self.assertEqual(coptic.from_gregorian(2017, 1, 7), (1733, 4, 29))
        self.assertEqual(coptic.to_gregorian(1727, 11, 11), (2011, 7, 18))

    def test_dublin_dc(self):
        self.assertEqual(dublin.from_gregorian(1900, 1, 1), 0.5)
        self.assertEqual(dublin.to_gregorian(1), (1900, 1, 1))
        self.assertEqual(dublin.to_jd(0), 2415020.0)

        self.assertEqual(
            dublin.to_jd(dublin.from_jd(self.c)),
            gregorian.to_jd(*dublin.to_gregorian(dublin.from_gregorian(*self.c_greg))),
        )

        self.assertEqual(dublin.to_gregorian(dublin.from_jd(1737936)), gregorian.from_jd(1737936))
        self.assertEqual(dublin.to_julian(dublin.from_jd(1737936)), julian.from_jd(1737936))

    def test_julian_day(self):
        self.assertEqual(julianday.from_gregorian(*self.c_greg), self.c)
        self.assertEqual(julianday.to_datetime(self.c), datetime(1492, 10, 21, tzinfo=timezone.utc))
        self.assertEqual(julianday.to_datetime(self.x), datetime(2016, 2, 29, tzinfo=timezone.utc))

        self.assertEqual(julianday.to_datetime(self.c + 0.25), datetime(1492, 10, 21, 6, tzinfo=timezone.utc))
        self.assertEqual(julianday.to_datetime(self.x + 0.525), datetime(2016, 2, 29, 12, 36, tzinfo=timezone.utc))

        dt = datetime(2014, 11, 8, 3, 37, tzinfo=timezone.utc)
        self.assertEqual(julianday.from_datetime(dt), 2456969.65069)

        self.assertEqual(julianday.to_datetime(self.x + 0.525), datetime(2016, 2, 29, 12, 36, tzinfo=timezone.utc))

    def test_month_length_julian(self):
        self.assertEqual(julian.month_length(1582, 10), 31)
        self.assertEqual(julian.month_length(1977, 2), 28)
        self.assertEqual(julian.month_length(1900, 2), 29)
        self.assertEqual(julian.month_length(1904, 2), 29)

    def test_month_length_islamic(self):
        self.assertEqual(islamic.month_length(1436, 1), 30)
        self.assertEqual(islamic.month_length(1436, 2), 29)
        self.assertEqual(islamic.month_length(1436, 12), 30)

    def test_monthcalendar_julian(self):
        self.assertEqual(julian.monthcalendar(1582, 10).pop(0).pop(1), 1)
        self.assertEqual(julian.monthcalendar(1582, 10).pop().pop(3), 31)

    def test_monthcalendar_islamic(self):
        self.assertEqual(islamic.monthcalendar(1436, 10).pop(0).pop(6), 1)
        self.assertEqual(islamic.monthcalendar(1436, 11).pop().pop(1), 30)

    def test_monthcalendar_hebrew(self):
        self.assertEqual(hebrew.monthcalendar(5775, 7).pop(0).pop(4), 1)
        self.assertEqual(hebrew.monthcalendar(5775, 7).pop().pop(0), 25)

    def test_returntype(self):
        self.assertSequenceType(coptic.from_gregorian(2020, 6, 4), int)
        self.assertSequenceType(hebrew.from_gregorian(2020, 6, 4), int)
        self.assertSequenceType(islamic.from_gregorian(2020, 6, 4), int)
        self.assertSequenceType(iso.from_gregorian(2020, 6, 4), int)
        self.assertSequenceType(julian.from_gregorian(2020, 6, 4), int)
        self.assertSequenceType(persian.from_gregorian(2020, 6, 4), int)
