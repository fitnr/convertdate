import unittest
from datetime import datetime
from convertdate import holidays

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
        assert h.columbus_day == (2014, 10, 13)

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

        H = holidays.Holidays()
        assert H.year == datetime.now().year
        assert str(self.h) == 'Holidays(2015)'

        H.set_year(2010)

        assert H.year == 2010

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

        assert holidays.columbus_day(2015, 'canada') == (2015, 10, 12)

        assert holidays.independence_day(2015) == (2015, 7, 4)
        assert holidays.independence_day(2015, True) == (2015, 7, 3)

    def test_thanksgiving(self):
        assert holidays.thanksgiving(2013) == (2013, 11, 28)
        assert holidays.thanksgiving(1939) == (1939, 11, 23)
        self.assertEqual(holidays.thanksgiving(1941), (1941, 11, 20))

        assert self.h.thanksgiving == (2015, 11, 26)

        assert holidays.thanksgiving(2015, 'canada') == (2015, 10, 12)

    def test_easter(self):
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
            (2034, 4, 9)
        ]
        for y, m, d in easters:
            self.assertEqual(holidays.easter(y), (y, m, d))

        self.assertEqual(self.h.easter, (2015, 4, 5))

    def test_jewish_holidays(self):
        # http://www.chabad.org/holidays/passover/pesach_cdo/aid/671901/jewish/When-is-Passover-in-2013-2014-2015-2016-and-2017.htm
        # the date here is the start of the holiday, so the eve=1 option is used
        passovers = [
            (2013, 3, 25),
            (2014, 4, 14),
            (2015, 4, 3),
            (2016, 4, 22),
            (2017, 4, 10)
        ]
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

        assert self.h.hanukkah == (2015, 12, 7)
        assert self.h.rosh_hashanah == (2015, 9, 14)
        assert self.h.yom_kippur == (2015, 9, 23)
        assert self.h.passover == (2015, 4, 4)

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
        assert self.h.columbus_day == (2015, 10, 12)
        assert self.h.veterans_day == (2015, 11, 11)
        assert self.h.martin_luther_king_day == (2015, 1, 19)

if __name__ == '__main__':
    unittest.main()
