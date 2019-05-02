# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import time
from convertdate import gregorian
from convertdate import bahai


class TestBahai(unittest.TestCase):

    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

    def test_trivial(self):
        assert 1 == 1

    def test_nawruz(self):
        nawruz_official = {
            2015: 21,
            2016: 20,
            2017: 20,
            2018: 21,
            2019: 21,
            2020: 20,
            2021: 20,
            2022: 21,
            2023: 21,
            2024: 20,
            2025: 20,
            2026: 21,
            2027: 21,
            2028: 20,
            2029: 20,
            2030: 20,
            2031: 21,
            2032: 20,
            2033: 20,
            2034: 20,
            2035: 21,
            2036: 20,
            2037: 20,
            2038: 20,
            2039: 21,
            2040: 20,
            2041: 20,
            2042: 20,
            2043: 21,
            2044: 20,
            2045: 20,
            2046: 20,
            2047: 21,
            2048: 20,
            2049: 20,
            2050: 20,
            2051: 21,
            2052: 20,
            2053: 20,
            2054: 20,
            2055: 21,
            2056: 20,
            2057: 20,
            2058: 20,
            2059: 20,
            2060: 20,
            2061: 20,
            2062: 20,
            2063: 20,
            2064: 20
        }

        for year in nawruz_official:
            bahaiyear = year - 1844 + 1
            date = bahai.to_gregorian(bahaiyear, 1, 1)
            assert (year, 3, nawruz_official[year]) == date


if __name__ == '__main__':
    unittest.main()
