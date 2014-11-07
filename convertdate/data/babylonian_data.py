# -*- coding: utf-8 -*-

# Months and years
#
MONTHS = [
    u"Nisānu",
    u"Āru",
    u"Simanu",
    u"Dumuzu",
    u'Abu',
    u"Ulūlu",
    u"Tišritum",
    u"Samna",
    u"Kislimu",
    u"Ṭebētum",
    u"Šabaṭu",
    u"Addaru",
]

INTERCALARIES = {
    'U': (u"Ulūlu II", 6),
    'u': (u"Ulūlu II", 6),
    'A': (u"Addaru II", 12),
    'a': (u"Addaru II", 12),
}

ASCII_MONTHS = [
    "Nisanu",
    "Aru",
    "Simanu",
    "Dumuzu",
    'Abu',
    "Ululu",
    "Tisritum",
    "Samna",
    "Kislimu",
    "Tebetum",
    "Sabatu",
    "Addaru",
]

ASCII_INTERCALARIES = {
    'U': ("Ululu II", 6),
    'u': ("Ululu II", 6),
    'A': ("Addaru II", 12),
    'a': ("Addaru II", 12),
}

'''Regnal stuff'''

SELEUCID_EPOCH = -311
ARSACID_EPOCH = -247
NABONASSAR_EPOCH = -625
JDC_START_OF_PROLEPTIC = 1737937.5
JDC_START_OF_REGNAL = 1492870.5

# key: year reign began
# value: name of ruler
rulers = {
    # No calendar information for these dudes
    # # IX
    # -748: u'Nabonassar',
    # -734: u'Nabu-nadin-zeri',

    # # X
    # -732: u'Nabu-mukin-zeri',
    # -729: u'Tiglath-Pileser III',
    # -727: u'Salmanassar V',
    # -722: u'Marduk-apal-iddina',
    # -710: u'Sargon II',
    # -705: u'Sennacherib',
    # -703: u'Bel-ibni',
    # -700: u'Aššur-nadim-šum',
    # -694: u'Nergal-ušezib',
    # -693: u'Mušezib-Marduk',

    # # Sack of babylon
    # -689: u'Sennacherib (II)',
    # -681: u'Asarhaddon',
    # -668: u'Šamaš-šum-ukin',
    # -648: u'Kandalānu',
    # -626: u'interregnum',

    # XI
    # Nabopolassar has a year 0
    -626: u'Nabopolassar',
    -604: u'Nebuchadnezzar II',
    -561: u'Amēl-Marduk',
    -559: u'Nergal-šar-usur', # Labashi-Marduk=year,4 of Nergal-shar-usur
    -555: u'Nabunaid',
    -538: u'Cyrus',

    # Achaemaenid
    -529: u'Cambyses',
    # Bardiya = year 8 of Cambyses
    # Nebuchadnezzar III=year 8 of Cambyses

    -521: u'Darius I', # Nebuchadnezzar IV=year 1 of Darius I
    -485: u'Xerxes',
    -464: u'Artaxerxes I',
    -423: u'Darius II',
    -404: u'Artaxerxes II Memnon',
    -358: u'Artaxerxes III Ochus',
    -337: u'Artaxerxes IV Arses',
    -335: u'Darius III',

    # Seleucid Dynasty
    -330: u'Alexander the Great', # Year 6 of Alexander = year 5 of Darius III
    -322: u'Philip III Arrhidaeus', # Year 1 of Philip = year 14 of Alexander

    # Year 1 of Alexander = year 8 of Philip
    -315: u'Alexander IV Aegus',
    # Years 6-10 of Alexander IV = years 1-5 of Seleucid Era
    -311: u'Seleucus I Nicator',
    -281: u'Antiochus I Soter',
    -261: u'Antiochus II Theos',

    # Year 65 Seleucid era = year 1 Arsacid era
    -246: u'Seleucus II Callinicus',
    -225: u'Seleucus III Soter',
    -222: u'Antiochus the Great',
    -187: u'Seleucus IV Philopater',
    -175: u'Antiochus IV Epiphanes',
    -164: u'Antiochus V Eupator',
    -160: u'Demetrius I Soter',
    -149: u'Alexander Balas',
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
    3: 'A', 5: 'A', 8: 'A', 11: 'A', 14: 'A', 17: 'U', 19: 'A'
}

# year: {
#    periods [ intercalations]
# }
# years are in BC (-1 == 1 BC)
#
intercalations = {
    # -747: {3: 'U'},
    # -728: {},  # No intercalary months
    # -709: {},  # No intercalary months
    # -690: {13: 'A'},
    # -671: {},  # No intercalary months

    # -652: {10: 'U'},
    -633: {9: 'a', 12: 'u', 15: 'U', 18: 'U'},
    -614: {1: 'u', 4: 'U', 6: 'u', 9: 'A', 12: 'U', 14: 'A', 17: 'U', 19: 'U'},
    -595: {3: 'u', 5: 'a', 8: 'A', 12: 'u', 14: 'A', 17: 'A', 19: 'A'},
    -576: {3: 'U', 5: 'A', 8: 'A', 13: 'U', 14: 'A', 17: 'A'},

    -557: {1: 'A', 3: 'A', 5: 'A', 8: 'A', 12: 'U', 14: 'A', 16: 'A'},
    -538: {2: 'U', 3: 'A', 6: 'A', 9: 'U', 12: 'U', 14: 'A', 16: 'A'},
    -519: {1: 'U', 3: 'A', 6: 'A', 9: 'U', 11: 'A', 14: 'A', 17: 'U'},
    -500: {1: 'A', 3: 'A', 6: 'A', 8: 'a', 9: 'A', 14: 'A', 17: 'U'},
    -481: {1: 'A', 3: 'a', 6: 'a', 8: 'A', 11: 'a', 14: 'a', 17: 'u', 19: 'a'},

    -462: {3: 'a', 6: 'a', 8: 'A', 11: 'a', 14: 'a', 17: 'u', 19: 'a'},
    -443: {3: 'a', 6: 'a', 8: 'a', 11: 'A', 14: 'a', 17: 'u', 19: 'A'},
    -424: {3: 'A', 6: 'A', 8: 'a', 11: 'A', 14: 'a', 17: 'u', 19: 'a'},
    -405: {3: 'a', 5: 'a', 8: 'a', 11: 'a', 14: 'a', 17: 'u', 19: 'A'},
    -386: {2: 'A', 6: 'A', 8: 'A', 11: 'A', 14: 'A', 17: 'U', 19: 'A'},

    -367: standard_intercalation

}
# standard 19 year cycle is used after -366
