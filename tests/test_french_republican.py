# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import time
from convertdate import gregorian
from convertdate import french_republican as fr

class TestFrenchRepublican(unittest.TestCase):
    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

        self.c_greg = (1492, 10, 21)
        self.c = gregorian.to_jd(*self.c_greg)
        self.x = gregorian.to_jd(2016, 2, 29)

        self.jdcs = range(2159677, 2488395, 2000)

    def test_french_republican(self):
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd))

        assert fr.from_gregorian(2014, 6, 14) == (222, 9, 26)

        self.assertEqual(gregorian.to_jd(1793, 9, 22), fr.to_jd(2, 1, 1))

        # 9 Thermidor II
        self.assertEqual(gregorian.to_jd(1794, 7, 27), fr.to_jd(2, 11, 9))

        for jd in range(2378822, 2488395, 2000):
            self.assertEqual(jd + 0.5, gregorian.to_jd(*gregorian.from_jd(jd + 0.5)))

    def test_french_republican_schematic(self):
        self.assertRaises(ValueError, fr.from_jd, self.jd, method=400)

        assert self.jd == fr.to_jd(*fr.from_jd(self.jd, method=128), method=128)
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd, method=100), method=100)
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd, method=4), method=4)

        j = self.jd - 265 * 150
        assert j == fr.to_jd(*fr.from_jd(j, method=128), method=128)
        assert j == fr.to_jd(*fr.from_jd(j, method=100), method=100)
        assert j == fr.to_jd(*fr.from_jd(j, method=4), method=4)

    def test_french_republican_names(self):
        self.assertEqual(fr.day_name(1, 1), "Raisin")
        assert fr.day_name(2, 1) == "Pomme"
        assert fr.day_name(4, 18) == "Pierre à chaux"
        assert fr.day_name(12, 15) == "Truite"
        assert fr.day_name(13, 1) == "La Fête de la Vertu"

if __name__ == '__main__':
    unittest.main()
