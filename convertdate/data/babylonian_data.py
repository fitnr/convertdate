# -*- coding: utf-8 -*-

# Months and years
# Month names from Parker & Dubberstein "Babylonian Chronology" (1924)
# and Sacha Stern "Calenders in Antiquity" 2012
MONTHS = [
    u"Nisannu",
    u"Aiaru",
    u"Simanu",
    u"Duzu",
    u'Abu',
    u"Ululu",
    u"Tashritu",
    u"Araḥsamnu",
    u"Kislimu",
    u"Ṭebetu",
    u"Shabaṭu",
    u"Addaru",
]

INTERCALARIES = {
    'U': (u"Ululu II", 6),
    'u': (u"Ululu II", 6),
    'A': (u"Addaru II", 12),
    'a': (u"Addaru II", 12),
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
NABOPOLASSAR_EPOCH = -624
JDC_START_OF_ANALEPTIC = 1737937.5
JDC_START_OF_REGNAL = 1492870.5

# key: year reign began
# value: name of ruler
rulers = {
    # No calendar information for these dudes
    # # IX
    # -746: u'Nabonassar',
    # -733: u'Nabu-nadin-zeri',

    # # X
    # -731: u'Nabu-mukin-zeri',
    # -728: u'Tiglath-Pileser III',
    # -726: u'Salmanassar V',
    # -721: u'Marduk-apal-iddina',
    # -709: u'Sargon II',
    # -704: u'Sennacherib',
    # -702: u'Bel-ibni',
    # -699: u'Aššur-nadim-šum',
    # -693: u'Nergal-ušezib',
    # -692: u'Mušezib-Marduk',

    # # Sack of babylon
    # -688: u'Sennacherib (II)',
    # -680: u'Asarhaddon',
    # -667: u'Šamaš-šum-ukin',
    # -647: u'Kandalānu',
    # -625: u'interregnum',

    # XI
    # Nabopolassar has a year 0
    -625: u'Nabopolassar',
    -603: u'Nebuchadnezzar II',
    -560: u'Amēl-Marduk',
    -558: u'Nergal-šar-usur', # Labashi-Marduk=year,4 of Nergal-shar-usur
    -554: u'Nabunaid',
    -537: u'Cyrus',

    # Achaemaenid
    -528: u'Cambyses',
    # Bardiya = year 8 of Cambyses
    # Nebuchadnezzar III=year 8 of Cambyses

    -520: u'Darius I', # Nebuchadnezzar IV=year 1 of Darius I
    -484: u'Xerxes',
    -463: u'Artaxerxes I',
    -422: u'Darius II',
    -403: u'Artaxerxes II Memnon',
    -357: u'Artaxerxes III Ochus',
    -336: u'Artaxerxes IV Arses',
    -334: u'Darius III',

    # Seleucid Dynasty
    -329: u'Alexander the Great', # Year 6 of Alexander = year 5 of Darius III
    -321: u'Philip III Arrhidaeus', # Year 1 of Philip = year 14 of Alexander

    # Year 1 of Alexander = year 8 of Philip
    -314: u'Alexander IV Aegus',
    # Years 6-10 of Alexander IV = years 1-5 of Seleucid Era
    -310: u'Seleucus I Nicator',
    -280: u'Antiochus I Soter',
    -260: u'Antiochus II Theos',

    # Year 65 Seleucid era = year 1 Arsacid era
    -245: u'Seleucus II Callinicus',
    -224: u'Seleucus III Soter',
    -221: u'Antiochus the Great',
    -186: u'Seleucus IV Philopater',
    -174: u'Antiochus IV Epiphanes',
    -163: u'Antiochus V Eupator',
    -159: u'Demetrius I Soter',
    -148: u'Alexander Balas',
    # : u'Demetrius II Nicator',
    # : u'Antiochus VI Dionysus',
    # : u'Diodotus Tryphon',
    # : u'Antiochus VII Sidetes',
    # : u'Demetrius II Nicator (II',
    # : u'Alexander II Zabinas',
    # : u'Seleucus V Philometor',
    # : u'Cleopatra Thea',
    # : u'Antiochus VIII Grypus',
    # : u'Antiochus IX Cyzicenus',
    # -95: u'Antiochus X Eusebes Philopator',
    # -95: u'Demetrius III Eucaerus',
    # -95: u'Disputed: Demetrius III Eucaerus, Antiochus X Eusebes Philopator ',
    # -92: u'',
    # -92: u'Philip I Philadelphus',
    # -87: u'Antiochus XII Dionysus',
    # -83: u'Tigranes of Armenia',
    # -69: u'Antiochus XIII Asiaticus',
    # -65: u'Philip II Philoromaeus'
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
    'evil-merodach': 'Amēl-Marduk',
    'nergal-šar-usur': 'Nergal-šar-usur',
    'nabonidus': 'Nabunaid',
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
