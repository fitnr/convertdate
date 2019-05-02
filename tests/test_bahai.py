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
            2021: 20
        }

        for year in nawruz_official:
            bahaiyear = year - 1844 + 1
            (gregorian_year, gregorian_month, gregorian_day) = bahai.to_gregorian(bahaiyear, 1, 1)
            assert gregorian_year == year
            assert gregorian_month == 3
            assert gregorian_day == nawruz_official[year]


if __name__ == '__main__':
    unittest.main()
