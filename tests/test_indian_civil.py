# -*- coding: utf-8 -*-
import time

from convertdate import gregorian, indian_civil

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

    def test_reflexive(self):
        self.reflexive(indian_civil)

    def test_inverse(self):
        self.assertEqual(self.jd, indian_civil.to_jd(*indian_civil.from_jd(self.jd)))

    def test_returntype(self):
        '''Check that from_jd, from_gregorian return integers'''
        self.assertSequenceType(indian_civil.from_jd(self.jd), int)
        self.assertSequenceType(indian_civil.from_gregorian(*self.c_greg), int)
        self.assertSequenceType(indian_civil.from_gregorian(2020, 6, 4), int)

    def test_negative_jd(self):
        self.assertSequenceEqual(indian_civil.from_jd(1.5), (-4791, 9, 5))
        self.assertSequenceEqual(indian_civil.from_jd(0.5), (-4791, 9, 4))
        self.assertSequenceEqual(indian_civil.from_jd(-0.5), (-4791, 9, 3))
        self.assertSequenceEqual(indian_civil.from_jd(-1.5), (-4791, 9, 2))

    def test_month_length_indian_civil(self):
        self.assertEqual(indian_civil.month_length(1922, 1), 31)
        self.assertEqual(indian_civil.month_length(1923, 1), 30)

    def test_monthcalendar_indian_civil(self):
        self.assertEqual(indian_civil.monthcalendar(1936, 8).pop(0).pop(4), 1)
        self.assertEqual(indian_civil.monthcalendar(1927, 2).pop(0).pop(4), 1)
        self.assertEqual(indian_civil.monthcalendar(1922, 1).pop().pop(4), 31)
