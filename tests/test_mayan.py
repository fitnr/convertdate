# -*- coding: utf-8 -*-
import time

from convertdate import gregorian, mayan

from . import CalTestCase


class TestMayan(CalTestCase):
    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.c_greg = (1492, 10, 21)
        self.c = gregorian.to_jd(*self.c_greg)

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

        self.jdcs = range(2159677, 2488395, 2000)

    def test_mayan_reflexive(self):
        assert self.jd == mayan.to_jd(*mayan.from_jd(self.jd))

        self.reflexive(mayan)

    def test_mayan_count(self):
        assert mayan.to_jd(13, 0, 0, 0, 0) == 2456282.5
        assert mayan.from_gregorian(2012, 12, 21) == (13, 0, 0, 0, 0)
        assert mayan.to_gregorian(13, 0, 0, 0, 0) == (2012, 12, 21)
        assert mayan.from_jd(self.c) == (11, 13, 12, 4, 13)

    def test_mayan_haab(self):
        # haab
        assert mayan.HAAB[2] == 'Zip'
        assert mayan.HAAB.index("Xul") == 5
        assert mayan.to_haab(self.c) == (16, "Sotz'")
        assert mayan.to_haab(2456282.5) == (3, "K'ank'in")

    def test_mayan_tzolkin(self):
        # tzolkin
        assert mayan.TZOLKIN[0] == "Imix'"
        assert mayan.to_tzolkin(self.c) == (12, "B'en")
        assert mayan.to_tzolkin(2456282.5) == (4, 'Ajaw')
        assert mayan.to_tzolkin(2456850.5) == (13, 'Lamat')

    def test_mayan_convenience(self):

        self.assertEqual(mayan.lc_to_haab(0, 0, 0, 0, 0), (8, "Kumk'u"))
        assert mayan.lc_to_tzolkin(0, 0, 0, 0, 0) == (4, "Ajaw")

        assert mayan.lc_to_tzolkin(9, 16, 12, 5, 17) == (6, "Kab'an")
        assert mayan.lc_to_haab(9, 16, 12, 5, 17) == (10, "Mol")

        assert mayan.lc_to_haab_tzolkin(9, 16, 12, 5, 17) == "6 Kab'an 10 Mol"

        assert mayan.translate_haab("Wayeb'") == 'Nameless'

    def test_mayan_predictions(self):
        assert mayan.next_haab("Sotz'", self.c) == 2266280.5

        for h in mayan.HAAB:
            assert mayan.to_haab(mayan.next_haab(h, self.c)) == (1, h)

        assert mayan.next_tzolkin_haab((13, "Ajaw"), (3, "Kumk'u"), 2456849.5) == 2463662.5

    def test_mayan_monthcalendar(self):
        calendar = mayan.haab_monthcalendar(13, 0, 2, 11, 13)
        row = calendar[0]
        square = row[-1]
        assert isinstance(row, list)
        assert isinstance(square, tuple)
        assert row[7][0] == 1

        assert mayan.to_jd(*calendar[-1][-1][-1]) == 19 + mayan.to_jd(13, 0, 2, 11, 13)
        self.assertEqual(square, (6, (13, "Etz'nab'"), (13, 0, 2, 11, 18)))

    def test_mayan_generators(self):
        lcg = mayan.longcount_generator(13, 0, 2, 11, 13)
        assert next(lcg) == (13, 0, 2, 11, 13)
        assert next(lcg) == (13, 0, 2, 11, 14)
        assert next(lcg) == (13, 0, 2, 11, 15)

        tzg = mayan.tzolkin_generator(9, "Ix")
        self.assertEqual(next(tzg), (9, "Ix"))
        assert next(tzg) == (10, "Men")
        assert next(tzg) == (11, "K'ib'")
