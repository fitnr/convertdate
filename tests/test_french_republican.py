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

        for jd in range(2378822, 2488395, 2000):
            self.assertEqual(jd + 0.5, gregorian.to_jd(*gregorian.from_jd(jd + 0.5)))

    def test_french_republican_start_of_years(self):
        assert fr.to_gregorian(1, 1, 1) == (1792, 9, 22)
        assert fr.to_gregorian(2, 1, 1) == (1793, 9, 22)
        assert fr.to_gregorian(3, 1, 1) == (1794, 9, 22)
        assert fr.to_gregorian(4, 1, 1) == (1795, 9, 23)
        assert fr.to_gregorian(5, 1, 1) == (1796, 9, 22)
        assert fr.to_gregorian(6, 1, 1) == (1797, 9, 22)
        assert fr.to_gregorian(7, 1, 1) == (1798, 9, 22)
        assert fr.to_gregorian(8, 1, 1) == (1799, 9, 23)
        assert fr.to_gregorian(9, 1, 1) == (1800, 9, 23)
        assert fr.to_gregorian(10, 1, 1) == (1801, 9, 23)
        assert fr.to_gregorian(11, 1, 1) == (1802, 9, 23)
        assert fr.to_gregorian(12, 1, 1) == (1803, 9, 24)
        assert fr.to_gregorian(13, 1, 1) == (1804, 9, 23)
        assert fr.to_gregorian(14, 1, 1) == (1805, 9, 23)

    def test_french_republican_known_leap(self):
        assert fr.to_gregorian(3, 13, 6) == (1795, 9, 22)
        assert fr.to_gregorian(7, 13, 6) == (1799, 9, 22)
        assert fr.to_gregorian(11, 13, 6) == (1803, 9, 23)

    def test_french_republican_famous_dates(self):
        self.assertEqual(gregorian.to_jd(1793, 9, 22), fr.to_jd(2, 1, 1))

        # 9 Thermidor II
        self.assertEqual(gregorian.to_jd(1794, 7, 27), fr.to_jd(2, 11, 9))

        # 18 Brumaire An VIII
        assert gregorian.to_jd(1799, 11, 9) == fr.to_jd(8, 2, 18)

        assert fr.to_jd(2, 9, 22) == gregorian.to_jd(1794, 6, 10)
        assert fr.to_jd(4, 1, 13) == gregorian.to_jd(1795, 10, 5)
        assert fr.to_gregorian(5, 12, 18) == (1797, 9, 4)
        assert fr.to_jd(6, 8, 22) == gregorian.to_jd(1798, 5, 11)

        # Coup of 30 Prairial VII
        self.assertEqual(fr.to_gregorian(7, 9, 30), (1799, 6, 18))

    def test_french_republican_months(self):
        self.assertEqual(fr.MOIS[0], "Vendémiaire")
        assert fr.MOIS[1] == "Brumaire"
        assert fr.MOIS[2] == 'Frimaire'
        assert fr.MOIS[3] == 'Nivôse'
        assert fr.MOIS[4] == 'Pluviôse'
        assert fr.MOIS[5] == 'Ventôse'
        assert fr.MOIS[6] == 'Germinal'
        assert fr.MOIS[7] == 'Floréal'
        assert fr.MOIS[8] == 'Prairial'
        assert fr.MOIS[9] == 'Messidor'
        assert fr.MOIS[10] == 'Thermidor'
        assert fr.MOIS[12] == 'Sansculottides'
        assert fr.MOIS[11] == "Fructidor"

    def test_french_republican_schematic_error(self):
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
