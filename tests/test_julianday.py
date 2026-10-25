# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, timedelta, timezone
from fractions import Fraction

from convertdate import julianday


class TestJulianDayDatetime(unittest.TestCase):
    def test_from_datetime_offsets(self):
        noon = datetime(2000, 1, 1, 12, tzinfo=timezone.utc)
        for offset in [-12, -8, 0, 5.5, 14]:
            with self.subTest(offset=offset):
                local = noon.astimezone(timezone(timedelta(hours=offset)))
                self.assertEqual(julianday.from_datetime(local), 2451545.0)
        self.assertEqual(julianday.from_datetime(noon.replace(tzinfo=None)), 2451545.0)

    def test_from_datetime_fraction(self):
        noon = datetime(2000, 1, 1, 12)
        for delta in [timedelta(minutes=37), timedelta(seconds=12), timedelta(microseconds=345678)]:
            with self.subTest(delta=delta):
                microseconds = delta // timedelta(microseconds=1)
                expected = float(Fraction(2451545) + Fraction(microseconds, 86400000000))
                self.assertEqual(julianday.from_datetime(noon + delta), expected)

    def test_to_datetime_fraction(self):
        noon = datetime(2000, 1, 1, 12, tzinfo=timezone.utc)
        for microseconds in [1, 123456, 999999, 59999999, 3599999999, 43199999999]:
            with self.subTest(microseconds=microseconds):
                jd = float(Fraction(2451545) + Fraction(microseconds, 86400000000))
                # Compare to the instant represented by the floating point JD.
                represented = round((Fraction.from_float(jd) - 2451545) * 86400000000)
                self.assertEqual(julianday.to_datetime(jd), noon + timedelta(microseconds=represented))
