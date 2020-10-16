# -*- coding: utf-8 -*-
import time
import unittest

from convertdate import julianday
from convertdate.armenian import (_valid_date, from_gregorian, from_jd, from_julian, leap, month_length, to_gregorian,
                                  to_jd, to_julian, tostring)

from . import CalTestCase


class TestArmenian(CalTestCase):
    def setUp(self):
        self.now = time.localtime()
        self.today = julianday.from_gregorian(self.now[0], self.now[1], self.now[2])

    def testValidDate(self):
        self.assertTrue(_valid_date(1, 1, 1))

        self.assertTrue(_valid_date(533, 1, 1, method="sarkawag"))

        with self.assertRaises(ValueError):
            _valid_date(401, 1, 1, method="sarkawag")

        with self.assertRaises(ValueError):
            _valid_date(30, 4, 31)

        with self.assertRaises(ValueError):
            _valid_date(536, 13, 6)

        self.assertTrue(_valid_date(536, 13, 6, method="sarkawag"))

    def testReflexive(self):
        self.assertEqual(self.today, to_jd(*from_jd(self.today)))
        self.assertEqual(self.today, to_jd(*from_jd(self.today, "sarkawag"), method="sarkawag"))
        for jd in range(2159677, 2488395, 2000):
            jd = jd + 0.5
            self.assertEqual(jd, to_jd(*from_jd(jd)))
            self.assertEqual(jd, to_jd(*from_jd(jd, "sarkawag"), method="sarkawag"))

    def testLeap(self):
        self.assertEqual(True, leap(600))
        self.assertEqual(False, leap(601))

    def testGregorian(self):
        self.assertEqual((2019, 11, 3), to_gregorian(1469, 4, 14))
        self.assertEqual((1469, 4, 14), from_gregorian(2019, 11, 3))

    def testMonthLength(self):
        self.assertEqual(30, month_length(600, 1))
        self.assertEqual(5, month_length(600, 13))
        self.assertEqual(6, month_length(600, 13, "sarkawag"))

    def testJulian(self):
        cases = [
            # first date of the calendar
            [(1, 1, 1), (552, 7, 11)],
            # last day of the year
            [(1, 13, 5), (553, 7, 10)],
            # leap year moves the calendar
            [(4, 13, 5), (556, 7, 9)],
            [(5, 1, 1), (556, 7, 10)],
            # check month boundaries for an entire year
            [(420, 1, 1), (971, 3, 29)],
            [(420, 1, 30), (971, 4, 27)],
            [(420, 2, 1), (971, 4, 28)],
            [(420, 2, 30), (971, 5, 27)],
            [(420, 3, 1), (971, 5, 28)],
            [(420, 3, 30), (971, 6, 26)],
            [(420, 4, 1), (971, 6, 27)],
            [(420, 4, 30), (971, 7, 26)],
            [(420, 5, 1), (971, 7, 27)],
            [(420, 5, 30), (971, 8, 25)],
            [(420, 6, 1), (971, 8, 26)],
            [(420, 6, 30), (971, 9, 24)],
            [(420, 7, 1), (971, 9, 25)],
            [(420, 7, 30), (971, 10, 24)],
            [(420, 8, 1), (971, 10, 25)],
            [(420, 8, 30), (971, 11, 23)],
            [(420, 9, 1), (971, 11, 24)],
            [(420, 9, 30), (971, 12, 23)],
            [(420, 10, 1), (971, 12, 24)],
            [(420, 10, 30), (972, 1, 22)],
            [(420, 11, 1), (972, 1, 23)],
            [(420, 11, 30), (972, 2, 21)],
            [(420, 12, 1), (972, 2, 22)],
            [(420, 12, 30), (972, 3, 22)],
            [(420, 13, 1), (972, 3, 23)],
            [(420, 13, 5), (972, 3, 27)],
            # check month boundaries around Julian leap year
            [(512, 13, 1), (1064, 2, 29)],
            [(512, 13, 2), (1064, 3, 1)],
            [(513, 1, 1), (1064, 3, 5)],
            # check the two calendars in 1084
            [(533, 6, 15), (1084, 8, 11)],
        ]

        for a, j in cases:
            self.assertEqual(a, from_julian(*j))

        for a, j in cases:
            self.assertEqual(j, to_julian(*a))

        self.assertEqual((533, 1, 1), from_julian(1084, 8, 11, method="sarkawag"))
        self.assertEqual((533, 13, 5), from_julian(1085, 8, 10, method="sarkawag"))
        self.assertEqual((536, 13, 6), from_julian(1088, 8, 10, method="sarkawag"))
        self.assertEqual((537, 1, 1), from_julian(1088, 8, 11, method="sarkawag"))

    def testTostring(self):
        self.assertEqual('14 trē 1469', tostring(1469, 4, 14))
