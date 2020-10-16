# -*- coding: utf-8 -*-
# reference: www.epochconverter.com/days/
import copy
import random
import unittest

from calendar import isleap
from convertdate import ordinal, gregorian

# COMMON_YEAR_ORDINALS[<key>][<dayofyear>] == key value for <dayofyear>
# I.e COMMON_YEAR_ORDINALS['day_of_month'][145] == 25 and COMMON_YEAR_ORDINALS['months'] == 5,
# in plain english, the 145th day of a common year is May 25th
COMMON_YEAR_ORDINALS = {'days': [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
                                 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
                                 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,
                                 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
                                 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
                                 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141,
                                 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158,
                                 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
                                 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192,
                                 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209,
                                 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226,
                                 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243,
                                 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260,
                                 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277,
                                 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294,
                                 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311,
                                 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328,
                                 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345,
                                 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362,
                                 363, 364, 365],
                        'day_of_month': [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                         21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,  # end of January
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28,  # end of February
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30, 31,  # end of March
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30,  # end of April
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30, 31,  # end of May
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30,  # end of June
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30, 31,  # end of July
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30, 31,  # end of August
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30,  # end of September
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30, 31,  # end of October
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30,  # end of November
                                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                         23, 24, 25, 26, 27, 28, 29, 30, 31,  # end of December
                                         ],
                        'months': [None, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                   1, 1, 1, 1, 1,  # end of January
                                   2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # end of February
                                   3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                                   3, 3, 3,  # end of March
                                   4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                                   4, 4,  # end of April
                                   5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                                   5, 5, 5,  # end of May
                                   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                                   6, 6,  # end of June
                                   7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                                   7, 7, 7,  # end of July
                                   8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                                   8, 8, 8,  # end of August
                                   9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                                   9, 9,  # end of September
                                   10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                                   10, 10, 10, 10, 10, 10, 10, 10, 10, 10,  # end of October
                                   11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
                                   11, 11, 11, 11, 11, 11, 11, 11, 11,  # end of November
                                   12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                                   12, 12, 12, 12, 12, 12, 12, 12, 12, 12  # end of December
                                   ]}

LEAP_YEAR_ORDINALS = copy.deepcopy(COMMON_YEAR_ORDINALS)
# insert February 29th
LEAP_YEAR_ORDINALS['days'].append(366)
LEAP_YEAR_ORDINALS['day_of_month'].insert(60, 29)
LEAP_YEAR_ORDINALS['months'].insert(60, 2)

assert len(COMMON_YEAR_ORDINALS['days']) == len(COMMON_YEAR_ORDINALS['day_of_month']) == \
       len(COMMON_YEAR_ORDINALS['months']) == 366

assert len(LEAP_YEAR_ORDINALS['days']) == len(LEAP_YEAR_ORDINALS['day_of_month']) == len(LEAP_YEAR_ORDINALS['months']) \
       == 367


class TestOrdinal(unittest.TestCase):
    @staticmethod
    def random_date_elements():
        """returns year, month, day, and dayofyear"""
        year = random.randint(-10000, 10000)
        dayofyear = random.randint(1, 365)
        month = COMMON_YEAR_ORDINALS['months'][dayofyear]
        day = COMMON_YEAR_ORDINALS['day_of_month'][dayofyear]
        if isleap(year):
            dayofyear = random.randint(1, 366)
            month = LEAP_YEAR_ORDINALS['months'][dayofyear]
            day = LEAP_YEAR_ORDINALS['day_of_month'][dayofyear]
        return year, month, day, dayofyear

    def test_to_jd(self):
        year, month, day, dayofyear = self.random_date_elements()
        self.assertEqual(ordinal.to_jd(year, dayofyear), gregorian.to_jd(year, month, day))

    def test_from_jd(self):
        year, month, day, dayofyear = self.random_date_elements()
        jd = gregorian.to_jd(year, month, day)
        self.assertEqual(ordinal.from_jd(jd), (year, dayofyear))

    def test_from_gregorian(self):
        year, month, day, dayofyear = self.random_date_elements()
        self.assertEqual(ordinal.from_gregorian(year, month, day), (year, dayofyear))

    def test_from_gregorian_for_december_31(self):
        common_year = random.randint(-10000, 10000) * 4 - 1
        leap_year = common_year * 4
        self.assertEqual(ordinal.from_gregorian(common_year, 12, 31), (common_year, 365))
        self.assertEqual(ordinal.from_gregorian(leap_year, 12, 31), (leap_year, 366))

    def test_to_gregorian(self):
        year, month, day, dayofyear = self.random_date_elements()
        self.assertEqual(ordinal.to_gregorian(year, dayofyear), (year, month, day))

    def test_to_gregorian_for_december_31(self):
        common_year = random.randint(-10000, 10000) * 4 - 1
        leap_year = common_year * 4
        self.assertEqual(ordinal.to_gregorian(common_year, 365), (common_year, 12, 31))
        self.assertEqual(ordinal.to_gregorian(leap_year, 366), (leap_year, 12, 31))


if __name__ == '__main__':
    unittest.main()