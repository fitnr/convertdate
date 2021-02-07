# -*- coding: utf-8 -*-
import math
import unittest
from convertdate import utils


class TestConvertdate(unittest.TestCase):
    def testCeil(self):
        self.assertEqual(utils.ceil(1.2), math.ceil(1.2))
        self.assertEqual(utils.ceil(-1.2), math.ceil(-1.2))

    def testTruncFloor(self):
        self.assertEqual(math.trunc(1.2), math.floor(1.2))
        self.assertNotEqual(math.trunc(-1.2), math.floor(-1.2))

    def test_jwday(self):
        self.assertEqual(utils.jwday(2459252.5), 6)
        self.assertEqual(utils.weekday_before(0, 2459252.5), 2459252.5 - 6)

        self.assertEqual(utils.jwday(2459252.5), 6)
        self.assertEqual(utils.weekday_before(0, 2459252.5), 2459252.5 - 6)

        self.assertEqual(utils.jwday(0.5), 1)
        self.assertEqual(utils.jwday(-0.5), 0)
        self.assertEqual(utils.jwday(-1.5), 6)
