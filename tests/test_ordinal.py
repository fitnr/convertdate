from calendar import isleap

from convertdate import gregorian, ordinal

from . import CalTestCase


class TestOrdinal(CalTestCase):
    def test_reflexive(self):
        self.reflexive(ordinal, range(2458849, 2458849 + 7289))

    def test_to_jd(self):
        self.assertEqual(ordinal.to_jd(1900, 1), 2415020.5)

    def test_from_jd(self):
        self.assertEqual(ordinal.from_jd(2415020.5), (1900, 1))

    def test_ordinal_to_gregorian(self):
        self.assertEqual(ordinal.to_gregorian(2013, 1), (2013, 1, 1))
        self.assertEqual(ordinal.to_gregorian(2013, 105), (2013, 4, 15))
        self.assertEqual(ordinal.to_gregorian(2013, 32), (2013, 2, 1))
        self.assertEqual(ordinal.to_gregorian(2012, 1), (2012, 1, 1))
        self.assertEqual(ordinal.to_gregorian(2012, 31), (2012, 1, 31))
        self.assertEqual(ordinal.to_gregorian(2012, 32), (2012, 2, 1))
        self.assertEqual(ordinal.to_gregorian(2012, 52), (2012, 2, 21))
        self.assertEqual(ordinal.to_gregorian(2012, 59), (2012, 2, 28))
        self.assertEqual(ordinal.to_gregorian(2012, 60), (2012, 2, 29))
        self.assertEqual(ordinal.to_gregorian(2012, 61), (2012, 3, 1))
        self.assertEqual(ordinal.from_gregorian(2013, 1, 1), (2013, 1))
        self.assertEqual(ordinal.from_gregorian(2013, 2, 1), (2013, 32))
        self.assertEqual(ordinal.from_gregorian(2013, 3, 1), (2013, 60))
        self.assertEqual(ordinal.from_gregorian(2013, 4, 15), (2013, 105))

    def test_jan_1(self):
        self.assertEqual(ordinal.from_gregorian(2000, 1, 1), (2000, 1))
        self.assertEqual(ordinal.from_gregorian(2004, 1, 1), (2004, 1))
        self.assertEqual(ordinal.from_gregorian(1, 1, 1), (1, 1))

    def test_dec_31(self):
        self.assertEqual(ordinal.to_gregorian(2001, 364), (2001, 12, 30), 'December 30, 2001')
        self.assertEqual(ordinal.to_gregorian(2004, 365), (2004, 12, 30))
        self.assertEqual(ordinal.to_gregorian(2001, 365), (2001, 12, 31))
        self.assertEqual(ordinal.to_gregorian(2004, 366), (2004, 12, 31))

        self.assertEqual(ordinal.from_gregorian(2001, 12, 30), (2001, 364))
        self.assertEqual(ordinal.from_gregorian(2004, 12, 30), (2004, 365))
        self.assertEqual(ordinal.from_gregorian(2001, 12, 31), (2001, 365))
        self.assertEqual(ordinal.from_gregorian(2004, 12, 31), (2004, 366))

    def test_leap(self):
        for year in range(1995, 2005):
            self.assertEqual(ordinal.from_gregorian(year, 2, 28), (year, 59))

            leap = 0
            if isleap(year):
                leap = 1
                self.assertEqual(ordinal.from_gregorian(year, 2, 29), (year, 60))

            self.assertEqual(ordinal.from_gregorian(year, 3, 1), (year, 60 + leap))

    def test_from_jd_dec_31_common_year(self):
        # An integer Julian day count for December 31 of a common year must map
        # to ordinal day 365, not the non-existent day 366. Regression for the
        # ``round(365.5) -> 366`` half-day rounding bug in ``from_jd``.
        for year in (2021, 2022, 2023, 2025, 2100, 2200):
            self.assertFalse(isleap(year))
            jd = gregorian.to_jd(year, 12, 31)  # ...5 (midnight) form
            self.assertEqual(ordinal.from_jd(jd), (year, 365))
            # and the integer JDN that gregorian maps to that same day
            self.assertEqual(ordinal.from_jd(int(jd) + 1), (year, 365))

    def test_from_jd_dec_31_leap_year(self):
        # Leap-year December 31 stays day 366.
        for year in (2020, 2024, 2000):
            self.assertTrue(isleap(year))
            self.assertEqual(ordinal.from_jd(gregorian.to_jd(year, 12, 31)), (year, 366))
            self.assertEqual(ordinal.from_jd(int(gregorian.to_jd(year, 12, 31)) + 1), (year, 366))

    def test_from_jd_consistent_with_gregorian(self):
        # For any Julian day -- integer count or ``.5`` midnight form -- the
        # ordinal date must describe the same calendar day as gregorian.from_jd,
        # and never yield a day of year beyond the length of its year.
        for jd in range(2415020, 2488395, 7):
            for j in (jd, jd + 0.5):
                year, doy = ordinal.from_jd(j)
                self.assertEqual((year, doy), ordinal.from_gregorian(*gregorian.from_jd(j)))
                self.assertLessEqual(doy, 366 if isleap(year) else 365)
                self.assertGreaterEqual(doy, 1)
