# -*- coding: utf-8 -*-
from math import trunc
from . import astro
from . import gregorian

EPOCH = 2375839.5

MOIS = [
    'Vendémiaire',
    'Brumaire',
    'Frimaire',
    'Nivôse',
    'Pluviôse',
    'Ventôse',
    'Germinal',
    'Floréal',
    'Prairial',
    'Messidor',
    'Thermidor',
    'Fructidor'
]


def annee_da_la_revolution(jd):
    '''Determine the year in the French revolutionary calendar in which a given Julian day falls.
        Returns an array of two elements:
       [0]  Année de la Révolution
       [1]  Julian day number containing equinox for this year.'''

    g = gregorian.from_jd(jd)
    guess = g[0] - 2

    lasteq = paris_equinoxe_jd(guess)
    while lasteq > jd:
        guess -= 1
        lasteq = paris_equinoxe_jd(guess)

    nexteq = lasteq - 1
    while not (lasteq <= jd and jd < nexteq):
        lasteq = nexteq
        guess += 1
        nexteq = paris_equinoxe_jd(guess)

    # not sure if python round and javascript math.round behave
    # identically?
    adr = round((lasteq - EPOCH) / astro.TropicalYear) + 1
    return (adr, lasteq)


def equinoxe_a_paris(year):
    '''Determine Julian day and fraction of the September equinox at the Paris meridian in a given Gregorian year.'''

    #  September equinox in dynamical time
    equJED = astro.equinox(year, 2)

    #  Correct for delta T to obtain Universal time
    equJD = equJED - (astro.deltat(year) / (24 * 60 * 60))

    #  Apply the equation of time to yield the apparent time at Greenwich
    equAPP = equJD + astro.equationOfTime(equJED)

    #  Finally, we must correct for the constant difference between
    #  the Greenwich meridian and that of Paris, 2°20'15" to the
    #  East.

    dtParis = (2 + (20 / 60.0) + (15 / (60 * 60.0))) / 360
    equParis = equAPP + dtParis

    return equParis


def paris_equinoxe_jd(year):
    '''Calculate Julian day during which the September equinox, reckoned from
    the Paris meridian,occurred for a given Gregorian year'''
    ep = equinoxe_a_paris(year)
    return trunc(ep - 0.5) + 0.5


def to_jd(an, mois, jour):
    '''Obtain Julian day from a given French Revolutionary calendar date.'''

    guess = EPOCH + (astro.TropicalYear * ((an - 1) - 1))
    adr = (an - 1, 0)

    while adr[0] < an:
        adr = annee_da_la_revolution(guess)
        guess = adr[1] + (astro.TropicalYear + 2)

    equinoxe = adr[1]

    jd = equinoxe + (30 * (mois - 1)) + (jour - 1)
    return jd


def from_jd(jd):
    '''Calculate date in the French Revolutionary
    calendar from Julian day.  The five or six
    "sansculottides" are considered a thirteenth
    month in the results of this function.'''
    jd = (trunc(jd) + 0.5)
    adr = annee_da_la_revolution(jd)

    an = int(adr[0])

    equinoxe = adr[1]
    mois = trunc((jd - equinoxe) / 30) + 1

    jour = int((jd - equinoxe) % 30) + 1

    return (an, mois, jour)

def decade(jour):
    return trunc(jour / 10) + 1


def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))

def to_gregorian(an, mois, jour):
    return gregorian.from_jd(to_jd(an, mois, jour))

def format(an, mois, jour):
    return "{0} {1} {2}".format(jour, MOIS[mois - 1], an)
