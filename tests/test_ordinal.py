from calendar import isleap

from convertdate import ordinal

from . import CalTestCase


class TestOrdinal(CalTestCase):
    def test_reflexive(self):
        self.reflexive(ordinal, range(2458849, 2458849 + 7289))

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
        self.assertEqual(ordinal.to_gregorian(2001, 364), (2001, 12, 30))
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
