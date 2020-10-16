# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from convertdate import holidays, julian


class TestHolidays(unittest.TestCase):
    def setUp(self):
        self.h = holidays.Holidays(2015)

    def test_nth_day_of_month(self):
        assert holidays.nth_day_of_month(4, 2, 4, 2014) == (2014, 4, 23)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 5, 3, 4, 2014)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 6, 2, 4, 2014)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 1, 7, 4, 2014)
        assert holidays.nth_day_of_month(4, 3, 11, 2014) == (2014, 11, 27)
        assert holidays.nth_day_of_month(0, 3, 11, 2014) == (2014, 11, 27)

    def test_holidays(self):
        h = holidays.Holidays(2014)
        self.assertEqual(h.christmas, (2014, 12, 25))
        assert h.thanksgiving == (2014, 11, 27)
        assert h.indigenous_peoples_day == (2014, 10, 13)

        assert h.independence_day == (2014, 7, 4)

        assert self.h.christmas == (2015, 12, 25)
        assert self.h.christmas_eve == (2015, 12, 24)
        assert self.h.new_years == (2015, 1, 1)
        assert self.h.new_years_eve == (2015, 12, 31)
        assert self.h.valentines_day == (2015, 2, 14)
        assert self.h.halloween == (2015, 10, 31)
        assert self.h.mothers_day == (2015, 5, 10)
        self.assertEqual(self.h.fathers_day, (2015, 6, 21))

    def test_class(self):
        h = holidays.Holidays()
        assert h.year == datetime.now().year
        assert str(self.h) == 'Holidays(2015)'

        h.set_year(2010)
        assert h.year == 2010

    def test_events(self):
        assert holidays.new_years(2013) == (2013, 1, 1)
        assert holidays.martin_luther_king_day(2015) == (2015, 1, 19)

        assert holidays.lincolns_birthday(2015) == (2015, 2, 12)
        assert holidays.valentines_day(2015) == (2015, 2, 14)
        assert holidays.washingtons_birthday(2015) == (2015, 2, 22)
        assert holidays.presidents_day(2015) == (2015, 2, 16)

        assert holidays.pulaski_day(2015) == (2015, 3, 2)
        assert self.h.pulaski_day == (2015, 3, 2)

        assert holidays.may_day(2015) == (2015, 5, 1)

        assert holidays.indigenous_peoples_day(2015, 'canada') == (2015, 10, 12)

        assert holidays.independence_day(2015) == (2015, 7, 4)
        assert holidays.independence_day(2015, True) == (2015, 7, 3)

    def test_thanksgiving(self):
        assert holidays.thanksgiving(2013) == (2013, 11, 28)
        assert holidays.thanksgiving(1939) == (1939, 11, 23)
        self.assertEqual(holidays.thanksgiving(1941), (1941, 11, 20))

        assert self.h.thanksgiving == (2015, 11, 26)

        assert holidays.thanksgiving(2015, 'canada') == (2015, 10, 12)

    def test_easterWestern(self):
        easters = [
            (1994, 4, 3),
            (1995, 4, 16),
            (1996, 4, 7),
            (1997, 3, 30),
            (1998, 4, 12),
            (1999, 4, 4),
            (2000, 4, 23),
            (2001, 4, 15),
            (2002, 3, 31),
            (2003, 4, 20),
            (2004, 4, 11),
            (2005, 3, 27),
            (2006, 4, 16),
            (2007, 4, 8),
            (2008, 3, 23),
            (2009, 4, 12),
            (2010, 4, 4),
            (2011, 4, 24),
            (2012, 4, 8),
            (2013, 3, 31),
            (2014, 4, 20),
            (2015, 4, 5),
            (2016, 3, 27),
            (2017, 4, 16),
            (2018, 4, 1),
            (2019, 4, 21),
            (2020, 4, 12),
            (2021, 4, 4),
            (2022, 4, 17),
            (2023, 4, 9),
            (2024, 3, 31),
            (2025, 4, 20),
            (2026, 4, 5),
            (2027, 3, 28),
            (2028, 4, 16),
            (2029, 4, 1),
            (2030, 4, 21),
            (2031, 4, 13),
            (2032, 3, 28),
            (2033, 4, 17),
            (2034, 4, 9),
            (2345, 4, 22),
        ]

        for y, m, d in easters:
            self.assertEqual(holidays.easter(y), (y, m, d))

    def test_easterEastern(self):
        easters = [
            (1999, 4, 11),
            (2000, 4, 30),
            (2001, 4, 15),
            (2002, 5, 5),
            (2003, 4, 27),
            (2004, 4, 11),
            (2005, 5, 1),
            (2006, 4, 23),
            (2007, 4, 8),
            (2008, 4, 27),
            (2009, 4, 19),
            (2010, 4, 4),
            (2011, 4, 24),
            (2012, 4, 15),
            (2013, 5, 5),
            (2014, 4, 20),
            (2015, 4, 12),
            (2016, 5, 1),
            (2017, 4, 16),
            (2018, 4, 8),
            (2019, 4, 28),
            (2020, 4, 19),
            (2021, 5, 2),
            (2022, 4, 24),
            (2023, 4, 16),
            (2024, 5, 5),
            (2025, 4, 20),
            (2026, 4, 12),
            (2027, 5, 2),
            (2028, 4, 16),
            (2029, 4, 8),
            (2030, 4, 28),
            (2031, 4, 13),
            (2032, 5, 2),
            (2033, 4, 24),
            (2034, 4, 9),
            (2035, 4, 29),
            (2036, 4, 20),
            (2037, 4, 5),
            (2038, 4, 25),
            (2039, 4, 17),
            (2056, 4, 9),
            (2156, 4, 11),
        ]

        for y, m, d in easters:
            self.assertEqual(holidays.easter(y, "orthodox"), (y, m, d))
            self.assertEqual(holidays.easter(y, "eastern"), (y, m, d))

        self.assertEqual(self.h.easter, (2015, 4, 5))

    def testNonChalcedonian(self):
        # In these years, Orthodox Easter falls on 6 April (Julian),
        # but Non-Chalcedonian churches celebrate it a week later on 13 Aprail
        years = (
            570,
            665,
            760,
            1007,
            1102,
            1197,
            1292,
            1539,
            1634,
            1729,
            1824,
            2071,
            2166,
            2261,
            2356,
        )

        for y in years:
            orthodox = julian.from_gregorian(*holidays.easter(y, "orthodox"))
            eastern = julian.from_gregorian(*holidays.easter(y, "eastern"))
            self.assertNotEqual(orthodox, eastern)
            self.assertEqual((y, 4, 6), orthodox)
            self.assertEqual((y, 4, 13), eastern)

        for y in years:
            self.assertEqual(holidays.easter(y + 1, "orthodox"), holidays.easter(y + 1, "eastern"))

    def test_jewish_holidays(self):
        # http://www.chabad.org/holidays/passover/pesach_cdo/aid/671901/jewish/When-is-Passover-in-2013-2014-2015-2016-and-2017.htm
        # the date here is the start of the holiday, so the eve=1 option is used
        passovers = [(2013, 3, 25), (2014, 4, 14), (2015, 4, 3), (2016, 4, 22), (2017, 4, 10)]
        for y, m, d in passovers:
            self.assertEqual(holidays.passover(y, eve=1), (y, m, d))

        rosh_hashanahs = [
            (2014, 9, 24),
            (2015, 9, 13),
            (2016, 10, 2),
            (2017, 9, 20),
        ]
        for y, m, d in rosh_hashanahs:
            self.assertEqual(holidays.rosh_hashanah(y, eve=1), (y, m, d))

        self.assertEqual(holidays.hanukkah(2015, True), (2015, 12, 6))
        self.assertEqual(holidays.hanukkah(2015), (2015, 12, 7))

        self.assertEqual(holidays.yom_kippur(2015), (2015, 9, 23))
        self.assertEqual(holidays.yom_kippur(2015, True), (2015, 9, 22))

        sukkots = [
            (2016, 10, 17),
            (2015, 9, 28),
        ]
        for y, m, d in sukkots:
            self.assertEqual(holidays.sukkot(y, eve=0), (y, m, d))

        shavuots = [(2016, 6, 12), (2015, 5, 24)]
        for y, m, d in shavuots:
            self.assertEqual(holidays.shavuot(y, eve=0), (y, m, d))

        purims = [(2017, 3, 12), (2016, 3, 24)]
        for y, m, d in purims:
            self.assertEqual(holidays.purim(y, eve=0), (y, m, d))

        tisha_bavs = [
            (2019, 8, 11),
            (2020, 7, 30),
            (2021, 7, 18),
            (2022, 8, 7),
            (2023, 7, 27),
        ]
        for y, m, d in tisha_bavs:
            self.assertEqual(holidays.tisha_bav(y, eve=0), (y, m, d))

        assert self.h.hanukkah == (2015, 12, 7)
        assert self.h.rosh_hashanah == (2015, 9, 14)
        assert self.h.yom_kippur == (2015, 9, 23)
        assert self.h.passover == (2015, 4, 4)

        assert self.h.tisha_bav == (2015, 7, 26)
        assert self.h.shemini_azeret == (2015, 10, 5)
        assert self.h.lag_baomer == (2015, 5, 7)
        assert self.h.tu_beshvat == (2015, 2, 4)

    def test_mexican_holidays(self):
        self.assertEqual(holidays.natalicio_benito_juarez(2015, False), (2015, 3, 21))
        self.assertEqual(holidays.natalicio_benito_juarez(2015), (2015, 3, 16))

        assert self.h.dia_constitucion == (2015, 2, 2)
        assert self.h.natalicio_benito_juarez == (2015, 3, 16)
        assert self.h.dia_independencia == (2015, 9, 16)
        assert self.h.dia_revolucion == (2015, 11, 16)

    def test_usa_holidays(self):
        assert self.h.independence_day == (2015, 7, 3)
        assert self.h.flag_day == (2015, 6, 14)
        assert self.h.election_day == (2015, 11, 3)
        assert self.h.presidents_day == (2015, 2, 16)
        assert self.h.washingtons_birthday == (2015, 2, 22)
        assert self.h.lincolns_birthday == (2015, 2, 12)
        assert self.h.memorial_day == (2015, 5, 25)
        assert self.h.labor_day == (2015, 9, 7)
        assert self.h.indigenous_peoples_day == (2015, 10, 12)
        assert self.h.veterans_day == (2015, 11, 11)
        assert self.h.martin_luther_king_day == (2015, 1, 19)

    def test_usa_holidays_observed(self):
        self.assertSequenceEqual(holidays.independence_day(2015), (2015, 7, 4))
        assert holidays.independence_day(2015, True) == (2015, 7, 3)
        assert holidays.washingtons_birthday(2015) == (2015, 2, 22)
        assert holidays.washingtons_birthday(2015, True) == (2015, 2, 16)
        assert holidays.washingtons_birthday(2020, True) == (2020, 2, 17)
        assert holidays.new_years(2022, True) == (2021, 12, 31)
        self.assertSequenceEqual(holidays.christmas(2021, True), (2021, 12, 24))

    def test_deprecated_columbus_day(self):
        with self.assertRaises(DeprecationWarning):
            holidays.columbus_day(2020)

    def test_islamic_holidays(self):
        """Test the dates of certain Islamic holidays."""
        holidays_2015 = {
            'eid_aladha': (2015, 9, 24),
            'ramadan': (2015, 6, 18),
            'eid_alfitr': (2015, 7, 18),
        }
        with self.subTest():
            for name, date in holidays_2015.items():
                self.assertEqual(getattr(self.h, name), date, name)

        h21 = holidays.Holidays(2021)
        holidays_2021 = {
            'eid_aladha': (2021, 7, 20),
            'ramadan': (2021, 4, 13),
            'eid_alfitr': (2021, 5, 13),
        }
        with self.subTest():
            for name, date in holidays_2021.items():
                self.assertEqual(getattr(h21, name), date, name)
