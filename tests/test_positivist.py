# -*- coding: utf-8 -*-
import unittest

from convertdate.data import positivist as data
from convertdate.positivist import EPOCH, dayname, festival, from_gregorian, from_jd, legal_date, to_gregorian, to_jd


class TestGregorian(unittest.TestCase):
    def setUp(self):
        pass

    def test_epoch(self):
        self.assertEqual(to_jd(1, 1, 1), EPOCH)
        self.assertEqual(to_jd(1, 1, 2), EPOCH + 1)
        self.assertEqual(to_jd(2, 1, 1), EPOCH + 365.0)
        self.assertEqual(from_jd(EPOCH), (1, 1, 1))

    def test_to_gregorian(self):
        self.assertEqual(to_gregorian(228, 13, 25), (2016, 12, 26))
        self.assertEqual(to_gregorian(228, 13, 25), (2016, 12, 26))

    def test_legaldate(self):
        self.assertTrue(legal_date(1, 1, 1))
        with self.assertRaises(ValueError):
            legal_date(0, 1, 1)

        with self.assertRaises(ValueError):
            legal_date(1, -1, 1)

        with self.assertRaises(ValueError):
            legal_date(1, 14, 3)

        with self.assertRaises(ValueError):
            legal_date(1, 16, 3)

    def test_from_jd(self):
        self.assertTrue(legal_date(*from_jd(2375479.5)))
        assert legal_date(*from_jd(2376479.5))
        assert legal_date(*from_jd(2378479.5))
        assert legal_date(*from_jd(2379479.5))

        with self.assertRaises(ValueError):
            from_jd(EPOCH - 0.5)

    def test_reflexive_jd(self):
        self.assertEqual(from_jd(to_jd(1, 1, 1)), (1, 1, 1))
        self.assertEqual(from_jd(to_jd(4, 1, 1)), (4, 1, 1))
        self.assertEqual(from_jd(to_jd(4, 14, 1)), (4, 14, 1))
        self.assertEqual(from_jd(to_jd(4, 14, 2)), (4, 14, 2))
        self.assertEqual(from_jd(to_jd(10, 1, 1)), (10, 1, 1))
        self.assertEqual(from_jd(to_jd(12, 1, 1)), (12, 1, 1))
        self.assertEqual(from_jd(to_jd(13, 1, 1)), (13, 1, 1))
        self.assertEqual(from_jd(to_jd(13, 1, 2)), (13, 1, 2))
        self.assertEqual(from_jd(to_jd(13, 1, 3)), (13, 1, 3))
        self.assertEqual(from_jd(to_jd(13, 1, 5)), (13, 1, 5))
        self.assertEqual(from_jd(to_jd(13, 1, 7)), (13, 1, 7))
        self.assertEqual(from_jd(to_jd(13, 1, 14)), (13, 1, 14))
        self.assertEqual(from_jd(to_jd(13, 1, 28)), (13, 1, 28))
        self.assertEqual(from_jd(to_jd(13, 2, 28)), (13, 2, 28))
        self.assertEqual(from_jd(to_jd(13, 6, 1)), (13, 6, 1))
        self.assertEqual(from_jd(to_jd(14, 1, 1)), (14, 1, 1))
        self.assertEqual(from_jd(to_jd(16, 1, 1)), (16, 1, 1))
        self.assertEqual(from_jd(to_jd(50, 1, 1)), (50, 1, 1))
        self.assertEqual(from_jd(to_jd(99, 1, 1)), (99, 1, 1))
        self.assertEqual(from_jd(to_jd(100, 1, 1)), (100, 1, 1))
        self.assertEqual(from_jd(to_jd(100, 13, 25)), (100, 13, 25))
        self.assertEqual(from_jd(to_jd(120, 13, 25)), (120, 13, 25))
        self.assertEqual(from_jd(to_jd(50, 13, 25)), (50, 13, 25))
        self.assertEqual(from_jd(to_jd(200, 1, 5)), (200, 1, 5))
        self.assertEqual(from_jd(to_jd(250, 14, 1)), (250, 14, 1))

    def test_reflexive_jd2(self):
        assert len(from_jd(2375479.5)) == 3
        self.assertEqual(to_jd(*from_jd(2375479.5)), 2375479.5)
        self.assertEqual(to_jd(*from_jd(2376479.5)), 2376479.5)
        self.assertEqual(to_jd(*from_jd(2378479.5)), 2378479.5)
        self.assertEqual(to_jd(*from_jd(2379479.5)), 2379479.5)

    def test_reflexive_gregorian(self):
        self.assertEqual(from_gregorian(*to_gregorian(100, 13, 25)), (100, 13, 25))
        self.assertEqual(from_gregorian(*to_gregorian(120, 13, 25)), (120, 13, 25))
        self.assertEqual(from_gregorian(*to_gregorian(50, 13, 25)), (50, 13, 25))
        self.assertEqual(from_gregorian(*to_gregorian(200, 1, 5)), (200, 1, 5))
        self.assertEqual(from_gregorian(*to_gregorian(250, 14, 1)), (250, 14, 1))

    def test_named_day(self):
        self.assertEqual(dayname(228, 13, 25), ('Bichat', "Félix Vicq-d'Azyr"))
        self.assertEqual(dayname(228, 1, 1), ('Moses', "Cadmus"))
        self.assertEqual(dayname(227, 1, 1), ('Moses', "Prometheus"))
        self.assertEqual(dayname(1, 1, 1), ('Moses', "Prometheus"))

    def test_festival(self):
        self.assertIsNone(festival(1, 2))
        self.assertEqual(festival(1, 1), data.FESTIVALS.get((1, 1)))
