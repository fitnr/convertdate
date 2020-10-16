# -*- coding: utf-8 -*-
import time
import unittest

from convertdate import french_republican as fr
from convertdate import gregorian

year_starts = [
    ((1, 1, 1), (1792, 9, 22)),
    ((2, 1, 1), (1793, 9, 22)),
    ((3, 1, 1), (1794, 9, 22)),
    ((4, 1, 1), (1795, 9, 23)),
    ((5, 1, 1), (1796, 9, 22)),
    ((6, 1, 1), (1797, 9, 22)),
    ((7, 1, 1), (1798, 9, 22)),
    ((8, 1, 1), (1799, 9, 23)),
    ((9, 1, 1), (1800, 9, 23)),
    ((10, 1, 1), (1801, 9, 23)),
    ((11, 1, 1), (1802, 9, 23)),
    ((12, 1, 1), (1803, 9, 24)),
    ((13, 1, 1), (1804, 9, 23)),
    ((14, 1, 1), (1805, 9, 23)),
]

leaps = [
    ((3, 13, 6), (1795, 9, 22)),
    ((7, 13, 6), (1799, 9, 22)),
    ((11, 13, 6), (1803, 9, 23)),
]

romme = [
    ((15, 1, 1), (1806, 9, 23)),
    ((15, 13, 5), (1807, 9, 22)),
    ((16, 1, 1), (1807, 9, 23)),
    ((16, 13, 6), (1808, 9, 22)),
    ((17, 1, 1), (1808, 9, 23)),
    ((17, 13, 5), (1809, 9, 22)),
    ((18, 1, 1), (1809, 9, 23)),
    ((19, 1, 1), (1810, 9, 23)),
    ((20, 1, 1), (1811, 9, 23)),
    ((20, 13, 6), (1812, 9, 22)),
    ((222, 1, 1), (2013, 9, 22)),
    ((223, 1, 1), (2014, 9, 22)),
    ((225, 1, 1), (2016, 9, 22)),
]

continuous = [
    ((15, 1, 1), (1806, 9, 23)),
    ((15, 13, 5), (1807, 9, 22)),
    ((15, 13, 6), (1807, 9, 23)),
    ((16, 1, 1), (1807, 9, 24)),
    ((17, 1, 1), (1808, 9, 23)),
    ((18, 1, 1), (1809, 9, 23)),
    ((19, 1, 1), (1810, 9, 23)),
    ((19, 13, 6), (1811, 9, 23)),
    ((20, 1, 1), (1811, 9, 24)),
    ((220, 1, 1), (2011, 9, 25)),
    ((221, 1, 1), (2012, 9, 24)),
    ((222, 1, 1), (2013, 9, 24)),
    ((223, 1, 1), (2014, 9, 24)),
    ((223, 13, 6), (2015, 9, 24)),
    ((224, 1, 1), (2015, 9, 25)),
    ((225, 1, 1), (2016, 9, 24)),
]

madler = [
    ((15, 1, 1), (1806, 9, 23)),
    ((15, 13, 6), (1807, 9, 23)),
    ((16, 1, 1), (1807, 9, 24)),
    ((16, 13, 5), (1808, 9, 22)),
    ((17, 1, 1), (1808, 9, 23)),
    ((18, 1, 1), (1809, 9, 23)),
    ((18, 13, 5), (1810, 9, 22)),
    ((19, 1, 1), (1810, 9, 23)),
    ((19, 13, 5), (1811, 9, 22)),
    ((20, 1, 1), (1811, 9, 23)),
    ((20, 13, 6), (1812, 9, 22)),
    ((222, 1, 1), (2013, 9, 23)),
    ((223, 1, 1), (2014, 9, 23)),
    ((224, 1, 1), (2015, 9, 23)),
    ((224, 13, 6), (2016, 9, 22)),
    ((225, 1, 1), (2016, 9, 23)),
]


class TestFrenchRepublican(unittest.TestCase):
    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

        self.x = gregorian.to_jd(2016, 2, 29)
        self.j = gregorian.to_jd(2015, 9, 24)

        # around the autumnal equinox
        self.start = 2457285

    def test_french_republican(self):
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd))
        assert fr.from_gregorian(2014, 6, 14) == (222, 9, 26)
        assert (2014, 6, 14) == fr.to_gregorian(222, 9, 26)

        assert (3, 13, 6) == fr.from_gregorian(1795, 9, 22)

        for jd in range(2378822, 2488395, 2000):
            self.assertEqual(jd + 0.5, gregorian.to_jd(*gregorian.from_jd(jd + 0.5)))

    def test_french_republican_leap(self):
        self.assertTrue(fr.leap(3))
        self.assertTrue(fr.leap(3, 'madler'))
        self.assertTrue(fr.leap(3, 'romme'))
        self.assertTrue(fr.leap(3, 'continuous'))

        self.assertTrue(fr.leap(7))
        self.assertTrue(fr.leap(7, 'madler'))
        self.assertTrue(fr.leap(7, 'romme'))
        self.assertTrue(fr.leap(7, 'continuous'))

        self.assertTrue(fr.leap(11))
        self.assertTrue(fr.leap(11, 'madler'))
        self.assertTrue(fr.leap(11, 'romme'))
        self.assertTrue(fr.leap(11, 'continuous'))

        self.assertFalse(fr.leap(4))
        self.assertFalse(fr.leap(14))

        self.assertTrue(fr.leap(15))
        self.assertTrue(fr.leap(15, 'madler'))
        self.assertFalse(fr.leap(15, 'romme'))
        self.assertTrue(fr.leap(15, 'continuous'))

        self.assertTrue(fr.leap(20))
        self.assertTrue(fr.leap(20, 'madler'))
        self.assertTrue(fr.leap(20, 'romme'))
        self.assertFalse(fr.leap(20, 'continuous'))

        self.assertFalse(fr.leap(23))
        self.assertFalse(fr.leap(23, 'madler'))
        self.assertFalse(fr.leap(23, 'romme'))
        self.assertTrue(fr.leap(23, 'continuous'))

        self.assertRaises(ValueError, fr.leap, 100, method='foo')

    def test_french_republican_decade(self):
        self.assertEqual(fr.decade(1), 1)

    def test_french_republican_format(self):
        self.assertEqual(fr.format(8, 2, 18), '18 Brumaire 8')

    def test_french_republican_to_jd_errors(self):
        self.assertRaises(ValueError, fr.to_jd, 100, 1, 0)
        self.assertRaises(ValueError, fr.to_jd, 100, 1, 31)
        self.assertRaises(ValueError, fr.to_jd, 100, 14, 1)
        self.assertRaises(ValueError, fr.to_jd, 4, 13, 6)
        self.assertRaises(ValueError, fr.to_jd, 100, 12, 1, method='foo')

    def test_french_republican_from_jd_errors(self):
        self.assertRaises(ValueError, fr.from_gregorian, 1789, 1, 1, 'romme')

    def test_french_republican_start_of_years_from_gregorian_equinoctal(self):
        for f, g in year_starts:
            self.assertEqual(f, fr.from_gregorian(*g))

    def test_french_republican_start_of_years_to_gregorian_equinoctal(self):
        for f, g in year_starts:
            self.assertEqual(g, fr.to_gregorian(*f))

    def test_french_republican_leap_days_from_gregorian_equinoctal(self):
        for f, g in leaps:
            self.assertEqual(f, fr.from_gregorian(*g))

    def test_french_republican_leap_days_to_gregorian_equinoctal(self):
        for f, g in leaps:
            self.assertEqual(g, fr.to_gregorian(*f))

    # Madler (128)

    def test_french_republican_leap_days_from_gregorian_madler(self):
        for f, g in leaps:
            self.assertEqual(f, fr.from_gregorian(*g, method='madler'))

    def test_french_republican_leap_days_to_gregorian_madler(self):
        for f, g in leaps:
            self.assertEqual(g, fr.to_gregorian(*f, method='madler'))

    def test_french_republican_schematic_madler_to_gregorian(self):
        for f, g in year_starts:
            self.assertEqual(g, fr.to_gregorian(*f, method=128))

        for f, g in madler:
            self.assertEqual(g, fr.to_gregorian(*f, method=128))

    def test_french_republican_schematic_madler_from_gregorian(self):
        for f, g in year_starts:
            self.assertEqual(g, fr.to_gregorian(*f, method=128))

        for f, g in madler:
            self.assertEqual(f, fr.from_gregorian(*g, method=128))

    def test_french_republican_schematic_madler(self):
        self.assertEqual(self.j, fr.to_jd(*fr.from_jd(self.j, method=128), method=128))
        self.assertEqual(self.x, fr.to_jd(*fr.from_jd(self.x, method=128), method=128))
        self.assertEqual(self.jd, fr.to_jd(*fr.from_jd(self.jd, method=128), method=128))

    # # Romme (100)

    def test_french_republican_leap_days_from_gregorian_romme(self):
        for f, g in leaps:
            self.assertEqual(f, fr.from_gregorian(*g, method=100))

    def test_french_republican_leap_days_to_gregorian_romme(self):
        for f, g in leaps:
            self.assertEqual(g, fr.to_gregorian(*f, method=100))

    def test_french_republican_schematic_romme_to_gregorian(self):
        for f, g in year_starts:
            self.assertEqual(g, fr.to_gregorian(*f, method=100))

        for f, g in romme:
            self.assertEqual(g, fr.to_gregorian(*f, method='romme'))

    def test_french_republican_schematic_romme_from_gregorian(self):
        for f, g in year_starts:
            self.assertEqual(f, fr.from_gregorian(*g, method='romme'))

        for f, g in romme:
            self.assertEqual(f, fr.from_gregorian(*g, method=100))

    def test_french_republican_schematic_romme(self):
        self.assertEqual(
            self.gregoriandate,
            fr.to_gregorian(*fr.from_gregorian(*self.gregoriandate, method=100), method=100),
        )

        self.assertEqual(self.jd, fr.to_jd(*fr.from_jd(self.jd, method='romme'), method=100))
        self.assertEqual(self.x, fr.to_jd(*fr.from_jd(self.x, method=100), method=100))
        assert self.j == fr.to_jd(*fr.from_jd(self.j, method=100), method=100)

    # Continuous (4)

    def test_french_republican_leap_days_from_gregorian_continuous(self):
        for f, g in leaps:
            self.assertEqual(f, fr.from_gregorian(*g, method=4))

    def test_french_republican_leap_days_to_gregorian_continuous(self):
        for f, g in leaps:
            self.assertEqual(g, fr.to_gregorian(*f, method=4))

    def test_french_republican_schematic_continuous_to_gregorian(self):
        for f, g in year_starts:
            self.assertEqual(g, fr.to_gregorian(*f, method=4))

        for f, g in continuous:
            self.assertEqual(g, fr.to_gregorian(*f, method='continuous'))

    def test_french_republican_schematic_continuous_from_gregorian(self):
        self.assertEqual((16, 1, 1), fr.from_gregorian(1807, 9, 24, method='continuous'))

        for f, g in year_starts:
            self.assertEqual(f, fr.from_gregorian(*g, method=4))

        for f, g in continuous:
            self.assertEqual(f, fr.from_gregorian(*g, method=4))

    def test_french_republican_schematic_continuous(self):
        self.assertEqual(gregorian.from_jd(self.jd), fr.to_gregorian(*fr.from_jd(self.jd, method=4), method=4))
        self.assertEqual(self.x, fr.to_jd(*fr.from_jd(self.x, method=4), method=4))

        assert self.j == fr.to_jd(*fr.from_jd(self.j, method='continuous'), method=4)

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

        assert (2, 9, 22) == fr.from_gregorian(1794, 6, 10)
        assert (4, 1, 13) == fr.from_gregorian(1795, 10, 5)
        assert (5, 12, 18) == fr.from_gregorian(1797, 9, 4)
        assert (6, 8, 22) == fr.from_gregorian(1798, 5, 11)

        # Coup of 30 Prairial VII
        self.assertEqual(fr.to_gregorian(7, 9, 30), (1799, 6, 18))

    def test_premier_da_la_annee(self):
        # Autumnal equinoxes in 1793 and 1794
        e0 = 2376204.5
        e1 = 2376569.5
        self.assertEqual(fr.premier_da_la_annee(e1 - 10), e0)
        self.assertEqual(fr.premier_da_la_annee(e1 + 100), e1)

    def test_french_republican_months(self):
        self.assertEqual(fr.MOIS[0], "Vendémiaire")
        self.assertEqual(fr.MOIS[1], "Brumaire")
        self.assertEqual(fr.MOIS[2], 'Frimaire')
        self.assertEqual(fr.MOIS[3], 'Nivôse')
        self.assertEqual(fr.MOIS[4], 'Pluviôse')
        self.assertEqual(fr.MOIS[5], 'Ventôse')
        self.assertEqual(fr.MOIS[6], 'Germinal')
        self.assertEqual(fr.MOIS[7], 'Floréal')
        self.assertEqual(fr.MOIS[8], 'Prairial')
        self.assertEqual(fr.MOIS[9], 'Messidor')
        self.assertEqual(fr.MOIS[10], 'Thermidor')
        self.assertEqual(fr.MOIS[12], 'Sansculottides')
        self.assertEqual(fr.MOIS[11], "Fructidor")

    def test_french_republican_schematic_error(self):
        self.assertRaises(ValueError, fr.from_jd, self.jd, method=400)
        self.assertRaises(ValueError, fr.from_jd, self.j, method=-1)

    def test_french_republican_names(self):
        self.assertEqual(fr.day_name(1, 1), "Raisin")
        self.assertEqual(fr.day_name(2, 1), "Pomme")
        self.assertEqual(fr.day_name(4, 18), "Pierre à chaux")
        self.assertEqual(fr.day_name(12, 15), "Truite")
        self.assertEqual(fr.day_name(13, 1), "La Fête de la Vertu")
