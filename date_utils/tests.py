import unittest
import time

import astro
import bahai
import french_republican as fr
import gregorian
import hebrew
import indian_civil
import iso
import julian
import mayan
import persian

def verify(jd, func, args_tuple):
    jd_cmp = func(*args_tuple)

    if jd != jd_cmp:
        e = "ERROR: {0}({1}) = {2} did not match jd ({3})"
        raise e.format(func, args_tuple, jd_cmp, jd)
    else:
        return 1


class CalTestCase(unittest.TestCase):

    def setUp(self):
        tm = time.localtime()
        self.gregoriandate = (tm[0], tm[1], tm[2])

        print "\nRunning date conversion test script:"
        print "-------------------------------------"

        print "gregorian date:", self.gregoriandate

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])
        print "julian day:", self.jd


    def test_gregorian(self):
        assert self.gregoriandate == gregorian.from_jd(self.jd)
        assert gregorian.to_jd(2000, 1, 1) == 2451544.5

    def test_mayan(self):
        assert self.jd == mayan.to_jd(*mayan.from_jd(self.jd))
        assert mayan.to_jd(13, 0, 0, 0, 0) == 2456282.5
        'mayan_haab', 'mayan_tzolkin'

    def test_french_republican(self):
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd))
        assert fr.from_jd(gregorian.to_jd(2014, 6, 14)) == (222, 10, 3, 8)
        # 9 Thermidor II
        assert gregorian.to_jd(1794, 7, 27) == fr.to_jd(2, 11, 1, 9)

    def test_hebrew(self):
        pass

    def test_islamic(self):
        pass

    def test_persian(self):
        pass

    def test_indian_civil(self):
        pass

    def test_iso(self):
        pass

    def test_julian(self):
        pass

    def test_bahai(self):
        pass


if __name__ == '__main__':
    unittest.main()

"python -m unittest date_utils.tests"
