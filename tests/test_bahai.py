# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import time
from convertdate import bahai


class TestBahai(unittest.TestCase):

    pairs = {
        (2041, 11, 27): (198, 14, 6),  # ascension of Abdu'l-Bahá 2041
        (2043, 11, 28): (200, 14, 6),  # ascension of Abdu'l-Bahá 2043
        (2038, 3, 1): (194, 20, 1),  # beginning of fast 2038
        (2039, 3, 2): (195, 20, 1),  # beginning of fast 2039
        (2040, 3, 1): (196, 20, 1),  # beginning of fast 2040
        (2041, 3, 1): (197, 20, 1),  # beginning of fast 2041
        (2042, 3, 1): (198, 20, 1),  # beginning of fast 2042
        (2043, 3, 2): (199, 20, 1),  # beginning of fast 2043
        (2031, 10, 17): (188, 12, 2),  # twin holy days, 2031
        (2031, 10, 18): (188, 12, 3)
    }

    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

    def test_gregorian_nawruz(self):
        nawruz_official = {
            20: [
                2016, 2017, 2020, 2021, 2024, 2025, 2028, 2029, 2030, 2032,
                2033, 2034, 2036, 2037, 2038, 2040, 2041, 2042, 2044, 2045,
                2046, 2048, 2049, 2050, 2052, 2053, 2054, 2056, 2057, 2058,
                2059, 2060, 2061, 2062, 2063, 2064
            ],
            21: [
                2015, 2018, 2019, 2022, 2023, 2026, 2027, 2031, 2035, 2039,
                2043, 2047, 2051, 2055
            ]
        }

        for date, gyears in nawruz_official.items():
            for gyear in gyears:
                self.assertEqual((3, date), bahai.gregorian_nawruz(gyear))

    def test_reflexive(self):
        for jd in range(2159677, 2488395, 1867):
            self.assertEqual(jd + 0.5, bahai.to_jd(*bahai.from_jd(jd + 0.5)))

    def test_to_gregorian(self):
        for g, b in self.pairs.items():
            self.assertEqual(g, bahai.to_gregorian(*b))

    def test_from_gregorian(self):
        for g, b in self.pairs.items():
            self.assertEqual(b, bahai.from_gregorian(*g))

    def test_month_length(self):
        for x in range(1, 19):
            self.assertEqual(bahai.month_length(2019, x), 19)

    def test_month_length_ha(self):
        official = {
            4: [
                2016, 2017, 2019, 2020, 2021, 2023, 2024, 2025, 2027, 2028, 2029, 2030, 2032,
                2033, 2034, 2036, 2037, 2038, 2040, 2041, 2042, 2044, 2045, 2046, 2048, 2049,
                2050, 2052, 2053, 2054, 2056, 2057, 2058, 2059, 2061, 2062, 2063, 2065
            ],
            5: [2018, 2022, 2026, 2031, 2035, 2039, 2043, 2047, 2051, 2055, 2060, 2064]
        }

        for length, gyears in official.items():
            for gyear in gyears:
                byear = gyear - 1844
                self.assertEqual(length, bahai.month_length(byear, 19))


if __name__ == '__main__':
    unittest.main()
