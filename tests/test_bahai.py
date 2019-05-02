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
            actual = bahai.to_gregorian(bahaiyear, 1, 1)
            expected = (year, 3, nawruz_official[year])
            self.assertEqual (expected, actual)


    def test_days_ha(self):
        days_official = {
            2016: 4,
            2017: 4,
            2018: 5,
            2019: 4,
            2020: 4,
            2021: 4,
            2022: 5,
            2023: 4,
            2024: 4,
            2025: 4,
            2026: 5,
            2027: 4,
            2028: 4,
            2029: 4,
            2030: 4,
            2031: 5,
            2032: 4,
            2033: 4,
            2034: 4,
            2035: 5,
            2036: 4,
            2037: 4,
            2038: 4,
            2039: 5,
            2040: 4,
            2041: 4,
            2042: 4,
            2043: 5,
            2044: 4,
            2045: 4,
            2046: 4,
            2047: 5,
            2048: 4,
            2049: 4,
            2050: 4,
            2051: 5,
            2052: 4,
            2053: 4,
            2054: 4,
            2055: 5,
            2056: 4,
            2057: 4,
            2058: 4,
            2059: 4,
            2060: 5,
            2061: 4,
            2062: 4,
            2063: 4,
            2064: 5,
            2065: 4
        }

        for year in days_official:
            bahaiyear = year - 1844  # there's some off-by-one business here
                                     # the Baha'i year of Ayam-i-Ha in 20XX 
                                     # starts in 20XX-1
            actual = bahai.month_length(bahaiyear, 19)
            expected = days_official[year]
            self.assertEqual (expected, actual)

if __name__ == '__main__':
    unittest.main()
