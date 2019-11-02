import unittest
import time
from convertdate import armenian
from convertdate import julianday


class TestArmenian(unittest.TestCase):
    def setUp(self):
        self.now = time.localtime()
        self.today = julianday.from_gregorian(self.now[0], self.now[1], self.now[2])

    def test_legal_date(self):
        self.assertTrue(armenian.legal_date(1, 1, 1))
        self.assertTrue(armenian.legal_date(533, 1, 1, method="sarkawag"))
        with self.assertRaises(ValueError):
            armenian.legal_date(401, 1, 1, method="sarkawag")
        with self.assertRaises(ValueError):
            armenian.legal_date(30, 4, 31)
        with self.assertRaises(ValueError):
            armenian.legal_date(536, 13, 6)
        self.assertTrue(armenian.legal_date(536, 13, 6, method="sarkawag"))

    def test_reflexive(self):
        self.assertEqual(self.today, armenian.to_jd(*armenian.from_jd(self.today)))
        self.assertEqual(self.today, armenian.to_jd(*armenian.from_jd(self.today, method="sarkawag"),
                                                    method="sarkawag"))
        for jd in range(2159677, 2488395, 2000):
            self.assertEqual(jd + 0.5, armenian.to_jd(*armenian.from_jd(jd + 0.5)))
            self.assertEqual(jd + 0.5, armenian.to_jd(*armenian.from_jd(jd + 0.5, method="sarkawag"),
                                                      method="sarkawag"))

    def test_cornercases(self):
        # first date of the calendar
        self.assertEqual((1, 1, 1), armenian.from_julian(552, 7, 11))
        # last day of the year
        self.assertEqual((1, 13, 5), armenian.from_julian(553, 7, 10))
        # leap year moves the calendar
        self.assertEqual((4, 13, 5), armenian.from_julian(556, 7, 9))
        self.assertEqual((5, 1, 1), armenian.from_julian(556, 7, 10))
        # check month boundaries for an entire year
        self.assertEqual((420, 1, 1), armenian.from_julian(971, 3, 29))
        self.assertEqual((420, 1, 30), armenian.from_julian(971, 4, 27))
        self.assertEqual((420, 2, 1), armenian.from_julian(971, 4, 28))
        self.assertEqual((420, 2, 30), armenian.from_julian(971, 5, 27))
        self.assertEqual((420, 3, 1), armenian.from_julian(971, 5, 28))
        self.assertEqual((420, 3, 30), armenian.from_julian(971, 6, 26))
        self.assertEqual((420, 4, 1), armenian.from_julian(971, 6, 27))
        self.assertEqual((420, 4, 30), armenian.from_julian(971, 7, 26))
        self.assertEqual((420, 5, 1), armenian.from_julian(971, 7, 27))
        self.assertEqual((420, 5, 30), armenian.from_julian(971, 8, 25))
        self.assertEqual((420, 6, 1), armenian.from_julian(971, 8, 26))
        self.assertEqual((420, 6, 30), armenian.from_julian(971, 9, 24))
        self.assertEqual((420, 7, 1), armenian.from_julian(971, 9, 25))
        self.assertEqual((420, 7, 30), armenian.from_julian(971, 10, 24))
        self.assertEqual((420, 8, 1), armenian.from_julian(971, 10, 25))
        self.assertEqual((420, 8, 30), armenian.from_julian(971, 11, 23))
        self.assertEqual((420, 9, 1), armenian.from_julian(971, 11, 24))
        self.assertEqual((420, 9, 30), armenian.from_julian(971, 12, 23))
        self.assertEqual((420, 10, 1), armenian.from_julian(971, 12, 24))
        self.assertEqual((420, 10, 30), armenian.from_julian(972, 1, 22))
        self.assertEqual((420, 11, 1), armenian.from_julian(972, 1, 23))
        self.assertEqual((420, 11, 30), armenian.from_julian(972, 2, 21))
        self.assertEqual((420, 12, 1), armenian.from_julian(972, 2, 22))
        self.assertEqual((420, 12, 30), armenian.from_julian(972, 3, 22))
        self.assertEqual((420, 13, 1), armenian.from_julian(972, 3, 23))
        self.assertEqual((420, 13, 5), armenian.from_julian(972, 3, 27))
        # check month boundaries around Julian leap year
        self.assertEqual((512, 13, 1), armenian.from_julian(1064, 2, 29))
        self.assertEqual((512, 13, 2), armenian.from_julian(1064, 3, 1))
        self.assertEqual((513, 1, 1), armenian.from_julian(1064, 3, 5))
        # check the two calendars in 1084
        self.assertEqual((533, 6, 15), armenian.from_julian(1084, 8, 11))
        self.assertEqual((533, 1, 1), armenian.from_julian(1084, 8, 11, method="sarkawag"))
        self.assertEqual((533, 13, 5), armenian.from_julian(1085, 8, 10, method="sarkawag"))
        self.assertEqual((536, 13, 6), armenian.from_julian(1088, 8, 10, method="sarkawag"))
        self.assertEqual((537, 1, 1), armenian.from_julian(1088, 8, 11, method="sarkawag"))
