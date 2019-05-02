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


if __name__ == '__main__':
    unittest.main()
