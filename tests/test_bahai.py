# -*- coding: utf-8 -*-
"""Test the Bahá’í calendar"""
import time
import unittest

from convertdate import bahai, gregorian

from . import CalTestCase


class TestBahai(CalTestCase):

    pairs = {
        (2041, 11, 27): (198, bahai.QAWL, 6),  # ascension of Abdu'l-Bahá 2041
        (2043, 11, 28): (200, bahai.QAWL, 6),  # ascension of Abdu'l-Bahá 2043
        (2038, 3, 1): (194, bahai.ALA, 1),  # beginning of fast 2038
        (2039, 3, 2): (195, bahai.ALA, 1),  # beginning of fast 2039
        (2040, 3, 1): (196, bahai.ALA, 1),  # beginning of fast 2040
        (2041, 3, 1): (197, bahai.ALA, 1),  # beginning of fast 2041
        (2042, 3, 1): (198, bahai.ALA, 1),  # beginning of fast 2042
        (2043, 3, 2): (199, bahai.ALA, 1),  # beginning of fast 2043
        (2031, 10, 17): (188, bahai.ILM, 2),  # twin holy days, 2031
        (2031, 10, 18): (188, bahai.ILM, 3),
        (2051, 11, 5): (208, bahai.QUDRAT, 2),
        (2052, 10, 24): (209, bahai.ILM, 10),
        (2053, 11, 11): (210, bahai.QUDRAT, 9),
        (2054, 11, 1): (211, bahai.ILM, 18),
        (2055, 10, 21): (212, bahai.ILM, 6),
        (2056, 11, 8): (213, bahai.QUDRAT, 6),
        (2057, 10, 29): (214, bahai.ILM, 15),
        (2058, 10, 18): (215, bahai.ILM, 4),
        (2059, 11, 6): (216, bahai.QUDRAT, 4),
        (2060, 10, 25): (217, bahai.ILM, 11),
        (2061, 10, 14): (218, bahai.MASHIYYAT, 19),
        (2062, 11, 2): (219, bahai.ILM, 19),
        (2063, 10, 23): (220, bahai.ILM, 9),
        (2064, 11, 10): (221, bahai.QUDRAT, 8),
    }

    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

    def test_reflexive(self):
        self.reflexive(bahai)

    def test_monthlength(self):
        self.assertEqual(bahai.month_length(1, 3), 19)
        self.assertEqual(bahai.month_length(1, 1), 19)

    def test_gregorian_nawruz(self):
        nawruz_official = {
            20: [
                2016,
                2017,
                2020,
                2021,
                2024,
                2025,
                2028,
                2029,
                2030,
                2032,
                2033,
                2034,
                2036,
                2037,
                2038,
                2040,
                2041,
                2042,
                2044,
                2045,
                2046,
                2048,
                2049,
                2050,
                2052,
                2053,
                2054,
                2056,
                2057,
                2058,
                2059,
                2060,
                2061,
                2062,
                2063,
                2064,
            ],
            21: [
                2015,
                2018,
                2019,
                2022,
                2023,
                2026,
                2027,
                2031,
                2035,
                2039,
                2043,
                2047,
                2051,
                2055,
            ],
        }

        for date, gyears in nawruz_official.items():
            for gyear in gyears:
                self.assertEqual((3, date), bahai.gregorian_nawruz(gyear))

    def test_ayyam_i_ha(self):
        # source: https://www.bahai.us/events/holy-days/
        # years with four days in Ayyám-i-Há
        # bahai_year: gregorian start of Ayyám-i-Há
        ayyamiha = [
            {"byear": 208, "gdate": (2052, 2, 26), "days": 4},
            {"byear": 209, "gdate": (2053, 2, 25), "days": 4},
            {"byear": 210, "gdate": (2054, 2, 25), "days": 4},
            {"byear": 211, "gdate": (2055, 2, 25), "days": 5},
            {"byear": 212, "gdate": (2056, 2, 26), "days": 4},
            {"byear": 213, "gdate": (2057, 2, 25), "days": 4},
            {"byear": 214, "gdate": (2058, 2, 25), "days": 4},
            {"byear": 215, "gdate": (2059, 2, 25), "days": 4},
            {"byear": 216, "gdate": (2060, 2, 25), "days": 5},
            {"byear": 217, "gdate": (2061, 2, 25), "days": 4},
            {"byear": 218, "gdate": (2062, 2, 25), "days": 4},
            {"byear": 219, "gdate": (2063, 2, 25), "days": 4},
            {"byear": 220, "gdate": (2064, 2, 25), "days": 5},
            {"byear": 221, "gdate": (2065, 2, 25), "days": 4},
        ]
        with self.subTest():
            for case in ayyamiha:
                start_jd = gregorian.to_jd(*case["gdate"])
                for i in range(case["days"]):
                    b = bahai.to_jd(case["byear"], bahai.AYYAMIHA, i + 1)
                    self.assertEqual(start_jd + i, b, "%s Ayyám-i-Há %s" % (i + 1, case["byear"]))

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
                2016,
                2017,
                2019,
                2020,
                2021,
                2023,
                2024,
                2025,
                2027,
                2028,
                2029,
                2030,
                2032,
                2033,
                2034,
                2036,
                2037,
                2038,
                2040,
                2041,
                2042,
                2044,
                2045,
                2046,
                2048,
                2049,
                2050,
                2052,
                2053,
                2054,
                2056,
                2057,
                2058,
                2059,
                2061,
                2062,
                2063,
                2065,
            ],
            5: [2018, 2022, 2026, 2031, 2035, 2039, 2043, 2047, 2051, 2055, 2060, 2064],
        }

        for length, gyears in official.items():
            for gyear in gyears:
                byear = gyear - 1844
                self.assertEqual(length, bahai.month_length(byear, 19))

    def test_returntype(self):
        self.assertSequenceType(bahai.from_gregorian(2020, 6, 4), int)
