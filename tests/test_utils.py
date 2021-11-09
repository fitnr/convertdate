# -*- coding: utf-8 -*-
import math
import unittest
from convertdate import utils


class TestConvertdate(unittest.TestCase):
    def test_amod(self):
        self.assertEqual(utils.amod(10, 5), 5)
        self.assertEqual(utils.amod(12, 3), 3)
        self.assertEqual(utils.amod(12, 4), 4)
        self.assertEqual(utils.amod(100, 4), 4)

    def test_jwday(self):
        self.assertEqual(utils.jwday(2459252.5), 6)
        self.assertEqual(utils.weekday_before(0, 2459252.5), 2459252.5 - 6)

        self.assertEqual(utils.jwday(2459252.5), 6)
        self.assertEqual(utils.weekday_before(0, 2459252.5), 2459252.5 - 6)

        self.assertEqual(utils.jwday(0.5), 1)
        self.assertEqual(utils.jwday(-0.5), 0)
        self.assertEqual(utils.jwday(-1.5), 6)
