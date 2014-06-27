from julian import Julianday

EPOCH = 584282.5
HAAB_MONTHS = ("Pop", "Uo", "Zip", "Zotz", "Tzec", "Xul",
                     "Yaxkin", "Mol", "Chen", "Yax", "Zac", "Ceh",
                     "Mac", "Kankin", "Muan", "Pax", "Kayab", "Cumku")

TZOLKIN_MONTHS = ("Imix", "Ik", "Akbal", "Kan", "Chicchan",
                        "Cimi", "Manik", "Lamat", "Muluc", "Oc",
                        "Chuen", "Eb", "Ben", "Ix", "Men",
                        "Cib", "Caban", "Etxnab", "Cauac", "Ahau")


def to_jd(baktun, katun, tun, uinal, kin):
    '''Determine Julian day from Mayan long count'''
    return Julianday(EPOCH + (baktun * 144000) + (katun * 7200) + (tun * 360) + (uinal * 20) + kin)

