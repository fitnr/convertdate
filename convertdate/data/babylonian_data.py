# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Months and years
# Month names from Parker & Dubberstein "Babylonian Chronology" (1924)
# and Sacha Stern "Calenders in Antiquity" 2012
MONTHS = [
    "Nisannu",
    "Aiaru",
    "Simanu",
    "Duzu",
    'Abu',
    "Ululu",
    "Tashritu",
    "Araḥsamnu",
    "Kislimu",
    "Ṭebetu",
    "Shabaṭu",
    "Addaru",
]

INTERCALARIES = {
    'U': ("Ululu II", 6),
    'u': ("Ululu II", 6),
    'A': ("Addaru II", 12),
    'a': ("Addaru II", 12),
}

ASCII_MONTHS = [
    "Nisannu",
    "Aiaru",
    "Simanu",
    "Duzu",
    'Abu',
    "Ululu",
    "Tashritu",
    "Arahsamnu",
    "Kislimu",
    "Tebetu",
    "Shabatu",
    "Addaru",
]

'''Regnal stuff'''
# These aren't the J year that the epoch started, but one smaller (greater abs val),
# Which lets us do straightforward addition/subtraction
SELEUCID_EPOCH = -311
ARSACID_EPOCH = -247
NABONASSAR_EPOCH = -746
JDC_START_OF_ANALEPTIC = 1737937.5
JDC_START_OF_REGNAL = 1492870.5

# key: year reign began
# value: name of ruler
rulers = {
    # # No calendar information for these dudes
    # 'Hammurabi': -1791,

    # # IX
    # 'Nabonassar': -746,
    # 'Nabu-nadin-zeri': -733,

    # # X
    # 'Nabu-mukin-zeri': -731,
    # 'Tiglath-Pileser III': -728,
    # 'Salmanassar V': -726,
    # 'Marduk-apal-iddina': -721,
    # 'Sargon II': -709,
    # 'Sennacherib': -704,
    # 'Bel-ibni': -702,
    # 'Aššur-nadim-šum': -699,
    # 'Nergal-ušezib': -693,
    # 'Mušezib-Marduk': -692,

    # Sack of babylon
    # -688: 'Sennacherib (II)',
    # 'Asarhaddon': -680,
    # 'Šamaš-šum-ukin': -667,
    # 'Kandalānu': -647,
    # 'interregnum': -625,

    # # XI
    # Nabopolassar has a year 0
    'Nabopolassar': -625,
    'Nebuchadnezzar II': -603,
    'Amēl-Marduk': -560,
    'Nergal-šar-usur': -558,  # Labashi-Marduk=year,4 of Nergal-shar-usur
    'Nabunaid': -554,
    'Cyrus': -537,

    # Achaemaenid
    'Cambyses': -528,
    # Bardiya = year 8 of Cambyses
    # Nebuchadnezzar III=year 8 of Cambyses

    'Darius I': -520,  # Nebuchadnezzar IV=year 1 of Darius I
    'Xerxes': -484,
    'Artaxerxes I': -463,
    'Darius II': -422,
    'Artaxerxes II Memnon': -403,
    'Artaxerxes III Ochus': -357,
    'Artaxerxes IV Arses': -336,
    'Darius III': -334,

    # Seleucid Dynasty
    'Alexander the Great': -329,  # Year 6 of Alexander = year 5 of Darius III
    'Philip III Arrhidaeus': -321,  # Year 1 of Philip = year 14 of Alexander

    # Year 1 of Alexander = year 8 of Philip
    'Alexander IV Aegus': -314,
    # Years 6-10 of Alexander IV = years 1-5 of Seleucid Era
    'Seleucus I Nicator': -310,
    'Antiochus I Soter': -280,
    'Antiochus II Theos': -260,

    # Year 65 Seleucid era = year 1 Arsacid era
    'Seleucus II Callinicus': -245,
    'Seleucus III Soter': -224,
    'Antiochus the Great': -221,
    'Seleucus IV Philopater': -186,
    'Antiochus IV Epiphanes': -174,
    'Antiochus V Eupator': -163,
    'Demetrius I Soter': -159,
    'Alexander Balas': -148,
    # 'Demetrius II Nicator',
    # 'Antiochus VI Dionysus',
    # 'Diodotus Tryphon',
    # 'Antiochus VII Sidetes',
    # 'Demetrius II Nicator (II',
    # 'Alexander II Zabinas',
    # 'Seleucus V Philometor',
    # 'Cleopatra Thea',
    # 'Antiochus VIII Grypus',
    # 'Antiochus IX Cyzicenus',
    # 'Antiochus X Eusebes Philopator': -95,
    # 'Demetrius III Eucaerus': -95,
    # 'Disputed: Demetrius III Eucaerus, Antiochus X Eusebes Philopator': -95,
    #  N/A: -92,
    # 'Philip I Philadelphus': -92,
    # 'Antiochus XII Dionysus': -87,
    # 'Tigranes of Armenia': -83,
    # 'Antiochus XIII Asiaticus': -69,
    # -65: 'Philip II Philoromaeus'
}


rulers_alt_names = {
    # 'nabu-nasir': 'Nabonassar',
    # 'nabu-nadin-zeri': 'Nabu-nadin-zeri',
    # 'nabu-mukin-zeri': 'Nabu-mukin-zeri',
    # 'tiglathpileser': 'Tiglath-Pileser III',
    # 'salmanassar v': 'Salmanassar V',
    # 'merodach-baladan': 'Marduk-apal-iddina', 'marduk-apal-iddina ii': 'Marduk-apal-iddina',
    # # 'sargon ii': 'Sargon II',
    # 'sin-ahhe-eriba': 'Sennacherib',
    # # 'bel-ibni': 'Bel-ibni',
    # 'ashur-nadin-shumi  ': 'Aššur-nadim-šum',
    # 'nergal-ushezib': 'Nergal-ušezib',
    # 'mushezib-marduk': 'Mušezib-Marduk',
    # # 'sennacherib': 'Sennacherib',
    # 'ashur-ahha-iddina': 'Asarhaddon',
    # 'shamash-shum-ukin': 'Šamaš-šum-ukin',
    # 'kandalanu': 'Kandalānu',
    # 'interregnum': 'interregnum',
    'nabopolassar': 'Nabopolassar',
    'nebuchadnezzar ii': 'Nebuchadnezzar II',
    'amel-marduk': 'Amēl-Marduk',
    'amēl-marduk': 'Amēl-Marduk',
    'evil-merodach': 'Amēl-Marduk',
    'nergal-šar-usur': 'Nergal-šar-usur',
    'nergal-shar-usur': 'Nergal-šar-usur',
    'nabonidus': 'Nabunaid',
    'nabunaid': 'Nabunaid',
    'cyrus': 'Cyrus',
    'cambyses ii': 'Cambyses',
    'darius i': 'Darius I',
    'xerxes': 'Xerxes',
    'artaxerxes i': 'Artaxerxes I',
    'darius ii': 'Darius II',
    'artaxerxes ii': 'Artaxerxes II Memnon', 'artaxerxes ii memnon': 'Artaxerxes II Memnon',
    'artaxerxes iii': 'Artaxerxes III Ochus', 'artaxerxes iii ochus': 'Artaxerxes III Ochus',
    'artaxerxes iv': 'Artaxerxes IV Arses', 'artaxerxes iv arses': 'Artaxerxes IV Arses',
    'darius iii': 'Darius III',
    'alexander iii the great': 'Alexander the Great',
    'philip iii arrhidaeus': 'Philip III Arrhidaeus',
    'alexander iv': 'Alexander IV Aegus',
    'alexander iv of macedon': 'Alexander IV Aegus',
    'alexander iv aegus': 'Alexander IV Aegus',
    'seleucus i': 'Seleucus I Nicator', 'seleucus i nicator': 'Seleucus I Nicator',
    'antiochus i': 'Antiochus I Soter', 'antiochus i soter': 'Antiochus I Soter',
    'antiochus ii': 'Antiochus II Theos', 'antiochus ii theos': 'Antiochus II Theos',
    'seleucus ii': 'Seleucus II Callinicus', 'seleucus ii callinicus': 'Seleucus II Callinicus',
    'seleucus iiir': 'Seleucus III Soter', 'seleucus iii soter': 'Seleucus III Soter',
    'antiochus iii': 'Antiochus the Great', 'antiochus the great': 'Antiochus the Great',
    'seleucus iv': 'Seleucus IV Philopater', 'seleucus iv philopater': 'Seleucus IV Philopater',
    'antiochus iv': 'Antiochus IV Epiphanes', 'antiochus iv epiphanes': 'Antiochus IV Epiphanes',
    'antiochus v': 'Antiochus V Eupator', 'antiochus v eupator': 'Antiochus V Eupator',
    'demetrius i': 'Demetrius I Soter', 'demetrius i soter': 'Demetrius I Soter',
    'alexander i balas': 'Alexander Balas', 'alexander balas': 'Alexander Balas',
    'antiochus vi epiphanes': 'Antiochus VI Dionysus', 'antiochus vi dionysus': 'Antiochus VI Dionysus',
    'antiochus vii euergetes': 'Antiochus VII Sidetes', 'antiochus vii sidetes': 'Antiochus VII Sidetes',
    'demetrius iii philopator': 'Demetrius III Eucaerus', 'demetrius iii eucaerus': 'Demetrius III Eucaerus',
    'seleucus vii philometor': 'Seleucus VII Kybiosaktes', 'seleucus vii kybiosaktes': 'Seleucus VII Kybiosaktes',
}

# First day of the Babylonian year in -366
# JD_START_OF_METONIC = 1587851.5

standard_intercalation = {
    0: 'A',
    3: 'A',
    6: 'A',
    8: 'A',
    11: 'A',
    14: 'A',
    17: 'U',
    # For the 3-year bonus cycle that occurs every 687 years
    21: 'A',
}

YEAR_LENGTH_LIST = [
    13, 12, 12,
    13, 12, 12,
    13, 12, 13,
    12, 12, 13,
    12, 12, 13,
    12, 12, 13,
    12, 12, 12, 13
]

# year: {
#    periods [ intercalations]
# }
# years are in BC (-1 == 1 BC)
#
# This is slightly edited from Plate I in Parker & Dubberstein
# This version of the cycle runs from 0-18. Year 19 of each cycle has been moved to year 0
# of the following cycle.
# The benefit of this is that the Seleucid era begins in year 0 of a cycle, simplifying arithmatic
intercalations = {
    # -747: {3: 'U'},
    # -728: {},  # No intercalary months
    # -709: {},  # No intercalary months
    # -690: {13: 'A'},
    # -671: {},  # No intercalary months

    # -652: {10: 'U'},
    -633: {9: 'a', 12: 'u', 15: 'U', 18: 'U'},
    -614: {1: 'u', 4: 'U', 6: 'u', 9: 'A', 12: 'U', 14: 'A', 17: 'U'},
    -595: {0: 'U', 3: 'u', 5: 'a', 8: 'A', 12: 'u', 14: 'A', 17: 'A'},
    -576: {0: 'A', 3: 'U', 5: 'A', 8: 'A', 13: 'U', 14: 'A', 17: 'A'},

    -557: {1: 'A', 3: 'A', 5: 'A', 8: 'A', 12: 'U', 14: 'A', 16: 'A'},
    -538: {2: 'U', 3: 'A', 6: 'A', 9: 'U', 12: 'U', 14: 'A', 16: 'A'},
    -519: {1: 'U', 3: 'A', 6: 'A', 9: 'U', 11: 'A', 14: 'A', 17: 'U'},
    -500: {1: 'A', 3: 'A', 6: 'A', 8: 'a', 9: 'A', 14: 'A', 17: 'U'},
    -481: {1: 'A', 3: 'a', 6: 'a', 8: 'A', 11: 'a', 14: 'a', 17: 'u'},

    -462: {0: 'a', 3: 'a', 6: 'a', 8: 'A', 11: 'a', 14: 'a', 17: 'u'},
    -443: {0: 'a', 3: 'a', 6: 'a', 8: 'a', 11: 'A', 14: 'a', 17: 'u'},
    -424: {0: 'A', 3: 'A', 6: 'A', 8: 'a', 11: 'A', 14: 'a', 17: 'u'},
    -405: {0: 'a', 3: 'a', 5: 'a', 8: 'a', 11: 'a', 14: 'a', 17: 'u'},
    -386: {0: 'A', 2: 'A', 6: 'A', 8: 'A', 11: 'A', 14: 'A', 17: 'U'},

    -367: standard_intercalation

}
# standard 19 year cycle is used after -366
