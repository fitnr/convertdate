# -*- coding: utf-8 -*-

# Most of this code is ported from Fourmilab's javascript calendar converter
# http://www.fourmilab.ch/documents/calendar/
# which was developed by John Walker
#
# The algorithms are believed to be derived from the following source:
# Meeus, Jean. Astronomical Algorithms . Richmond: Willmann-Bell, 1991. ISBN 0-943396-35-2.
#    The essential reference for computational positional astronomy.
#
import unittest

JDCS = range(2159677, 2488395, 2000)


class CalTestCase(unittest.TestCase):
    def reflexive(self, module, dates=None):
        """Check that the to_func and from_func work for a range of Julian dates."""
        to_func = getattr(module, 'to_jd')
        from_func = getattr(module, 'from_jd')
        dates = dates or JDCS
        for j in dates:
            j = j + 0.5
            self.assertEqual(j, to_func(*from_func(j)), 'checking from_jd(to_jd({0}))'.format(j))

    def assertSequenceType(self, seq, cls):
        '''Assert that all members of `seq` are of the type `cls`.'''
        for x in seq:
            self.assertIs(type(x), cls)
