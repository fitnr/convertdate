# -*- coding: utf-8 -*-
# JDC of the start of each lunation

# Some concepts from
# http://www.staff.science.uu.nl/~gent0113/babylon/downloads/babylonian_chronology_pd1956.dat
# http://www.staff.science.uu.nl/~gent0113/babylon/addfiles/babycal_dat.js

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

'''Regnal stuff'''

SELEUCID_EPOCH = -311
ARASCID_EPOCH = -247
NABONASSAR_EPOCH = -749
JDC_START_OF_PROLEPTIC = 1737937.5
JDC_START_OF_REGNAL = 1492870.5

# Labashi-Marduk=year,4 of Nergal-shar-usur

# Bardiya = year 8 of Cambyses
# Nebuchadnezzar Til=year 8 of Cambyses

# Nebuchadnezzar IV=year 1 of Darius I

# Year 6 of Alexander I = year 5 of Darius III
# Year 1 of Philip = year 14 of Alexander I
# Year 1 of Alexander II = year 8 of Philip

# Years 6-10 of Alexander II = years 1-5 of Seleucid Era

# Year 65 Seleucid era = year 1 Arsacid era

# key: year reign began
# value: name of ruler
rulers = {
    # IX
    -749: u'Nabonassar',
    -735: u'Nabu-nadin-zeri',

    # X
    -733: u'Nabu-mukin-zeri',
    -730: u'Tiglath-Pileser III',
    -728: u'Salmanassar V',
    -723: u'Marduk-apal-iddina',
    -711: u'Sargon II',
    -706: u'Sennacherib',
    -704: u'Bel-ibni',
    -701: u'Aššur-nadim-šum',
    -695: u'Nergal-ušezib',
    -694: u'Mušezib-Marduk',
    # Sack of babylon
    -690: u'Sennacherib (II)',
    -682: u'Asarhaddon',
    -669: u'Šamaš-šum-ukin',
    -649: u'Kandalānu',
    -627: u'interregnum',

    # XI
    -626: u'Nabopolassar',
    -605: u'Nebuchadnezzar II',
    -562: u'Amēl-Marduk',
    -560: u'Nergal-šar-usur',
    -556: u'Nabunaid',
    -539: u'Cyrus',

    # Achaemaenid
    -530: u'Cambyses',
    -522: u'Darius I',
    -486: u'Xerxes',
    -465: u'Artaxerxes I',
    -424: u'Darius II',
    -405: u'Artaxerxes II Memnon',
    -359: u'Artaxerxes III Ochus',
    -338: u'Artaxerxes IV Arses',
    -336: u'Darius III',

    # Seleucid
    -331: u'Alexander the Great',
    -323: u'Philip III Arrhidaeus',
    -316: u'Alexander IV Aegus',
    -312: u'Seleucus I Nicator',
    -282: u'Antiochus I Soter',
    -262: u'Antiochus II Theos',
    -247: u'Seleucus II Callinicus',
    -226: u'Seleucus III Soter',
    -223: u'Antiochus the Great',
    -188: u'Seleucus IV Philopater',
    -176: u'Antiochus IV Epiphanes',
    -165: u'Antiochus V Eupator',
    -161: u'Demetrius I Soter',
    -150: u'Alexander Balas',
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
    # bc95: u'Antiochus X Eusebes Philopator',
    # bc95: u'Demetrius III Eucaerus',
    # bc95: u'Disputed: Demetrius III Eucaerus, Antiochus X Eusebes Philopator ',
    # bc92: u'',
    # bc92: u'Philip I Philadelphus',
    # bc87: u'Antiochus XII Dionysus',
    # bc83: u'Tigranes of Armenia',
    # bc 69: u'Antiochus XIII Asiaticus',
    # bc 65: u'Philip II Philoromaeus'
}


rulers_alt_names = {
    'nabu-nasir': 'Nabonassar',
    'nabu-nadin-zeri': 'Nabu-nadin-zeri',
    'nabu-mukin-zeri': 'Nabu-mukin-zeri',
    'tiglathpileser': 'Tiglath-Pileser III',
    'salmanassar v': 'Salmanassar V',
    'merodach-baladan': 'Marduk-apal-iddina', 'marduk-apal-iddina ii': 'Marduk-apal-iddina',
    # 'sargon ii': 'Sargon II',
    'sin-ahhe-eriba': 'Sennacherib',
    # 'bel-ibni': 'Bel-ibni',
    'ashur-nadin-shumi  ': 'Aššur-nadim-šum',
    'nergal-ushezib': 'Nergal-ušezib',
    'mushezib-marduk': 'Mušezib-Marduk',
    # 'sennacherib': 'Sennacherib',
    'ashur-ahha-iddina': 'Asarhaddon',
    'shamash-shum-ukin': 'Šamaš-šum-ukin',
    'kandalanu': 'Kandalānu',
    'interregnum': 'interregnum',
    'nabopolassar': 'Nabopolassar',
    'nebuchadnezzar ii': 'Nebuchadnezzar II',
    'amel-marduk': 'Amēl-Marduk', 'evil-merodach': 'Amēl-Marduk',
    'nergal-šar-usur': 'Nergal-šar-usur',
    'nabonidus': 'Nabunaid',
    # 'cyrus': 'Cyrus',
    'cambyses ii': 'Cambyses',
    # 'darius i': 'Darius I',
    # 'xerxes': 'Xerxes',
    'artaxerxes i': 'Artaxerxes I',
    'darius ii': 'Darius II',
    'artaxerxes ii memnon': 'Artaxerxes II Memnon',
    'artaxerxes iii ochus': 'Artaxerxes III Ochus',
    'artaxerxes iv arses': 'Artaxerxes IV Arses',
    'darius iii': 'Darius III',
    'alexander iii the great': 'Alexander the Great',
    'philip iii arrhidaeus': 'Philip III Arrhidaeus',
    'alexander iv': 'Alexander IV Aegus',
    'seleucus i': 'Seleucus I Nicator',
    'antiochus i': 'Antiochus I Soter',
    'antiochus ii': 'Antiochus II Theos',
    'seleucus ii': 'Seleucus II Callinicus',
    'seleucus iiir': 'Seleucus III Soter',
    'antiochus the great': 'Antiochus the Great',
    'seleucus iv': 'Seleucus IV Philopater',
    'antiochus iv': 'Antiochus IV Epiphanes',
    'antiochus v': 'Antiochus V Eupator',
    'demetrius i': 'Demetrius I Soter',
    'alexander balas': 'Alexander Balas',
    'antiochus vi epiphanes': 'Antiochus VI Dionysus',
    'antiochus vii euergetes': 'Antiochus VII Sidetes',
    'demetrius iii philopator': 'Demetrius III Eucaerus',
    'seleucus vii philometor': 'Seleucus VII Kybiosaktes',
}

# First day of the Babylonian year in -366
JD_START_OF_METONIC = 1587851.5

standard_intercalation = {
    3: 'A', 5: 'A', 8: 'A', 11: 'A', 14: 'A', 17: 'U', 19: 'A'
}

# year: {
#    periods [ intercalations]
# }
# years are astronomical (-1 = 2 BC)
#
intercalations = {
    -747: {3: 'U'},
    -728: {},  # No intercalary months
    -709: {},  # No intercalary months
    -690: {13: 'A'},
    -671: {},  # No intercalary months

    -652: {10: 'U'},
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
