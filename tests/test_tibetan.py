# -*- coding: utf-8 -*-
import time

from convertdate import gregorian, tibetan

import unittest

class TestConvertdate(unittest.TestCase):
    testdate = [
        [(2022, 1, 1), (2021, 10, False, 29, False)],
        [(2022, 1, 31), (2021, 11, False, 29, False)],
        [(2022, 2, 8), (2021, 12, False, 8, True)],
        [(2022, 2, 9), (2021, 12, False, 8, False)],
        [(2022, 3, 3), (2022, 1, False, 1, False)],
        [(1921, 7, 7), (1921, 6, False, 2, False)],
        [(1959, 3, 10), (1959, 2, False, 1, False)],
        [(1959, 2, 6), (1958, 12, False, 29, False)],
        [(1959, 1, 11), (1958, 12, False, 3, False)],
    ]

    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

    def test_inverse(self):
        self.assertEqual(self.jd, tibetan.to_jd(*tibetan.from_jd(self.jd)))

    def test_gregorian(self):
        for g, t in self.testdate:
            self.assertSequenceEqual(tibetan.from_gregorian(*g), t)
            self.assertSequenceEqual(tibetan.to_gregorian(*t), g)

    def test_month_length_tibetan(self):
        self.assertEqual(tibetan.month_length(1921, 6, False), 29)
        self.assertEqual(tibetan.month_length(1921, 7, True), 30)
