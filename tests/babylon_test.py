from convertdate import dublin
from convertdate import julian
from convertdate import utils
from convertdate.babylon import *
import ephem

def define_counts():
    y = [
        julian.to_jd(-130 - 1, 4, 16),
        julian.to_jd(-131 - 1, 4, 4),
        julian.to_jd(-132 - 1, 3, 25),
        julian.to_jd(-133 - 1, 4, 13),
        julian.to_jd(-134 - 1, 4, 3),
        julian.to_jd(-135 - 1, 4, 21),
        julian.to_jd(-136 - 1, 4, 10),
        julian.to_jd(-137 - 1, 3, 30),
        julian.to_jd(-138 - 1, 4, 18),
        julian.to_jd(-139 - 1, 4, 6),
        julian.to_jd(-140 - 1, 3, 26),
        julian.to_jd(-141 - 1, 4, 14),
        julian.to_jd(-142 - 1, 4, 4),
        julian.to_jd(-143 - 1, 4, 22),
        julian.to_jd(-144 - 1, 4, 11),
        julian.to_jd(-145 - 1, 4, 1),
        julian.to_jd(-146 - 1, 4, 20),
        julian.to_jd(-147 - 1, 4, 8),
        julian.to_jd(-148 - 1, 3, 28)
    ]

    s = [
        julian.to_jd(20 + 25, 4, 18),
        julian.to_jd(20 + 26, 4, 8),
        julian.to_jd(20 + 27, 3, 28),
        julian.to_jd(20 + 28, 4, 15),
        julian.to_jd(20 + 29, 4, 5),
        julian.to_jd(20 + 30, 3, 25),
        julian.to_jd(20 + 31, 4, 12),
        julian.to_jd(20 + 32, 4, 1),
        julian.to_jd(20 + 33, 4, 19),
        julian.to_jd(20 + 34, 4, 9),
        julian.to_jd(20 + 35, 3, 30),
        julian.to_jd(20 + 36, 4, 17),
        julian.to_jd(20 + 37, 4, 6),
        julian.to_jd(20 + 38, 3, 26),
        julian.to_jd(20 + 39, 4, 14),
        julian.to_jd(20 + 40, 4, 2),
        julian.to_jd(20 + 41, 4, 21),
        julian.to_jd(20 + 42, 4, 10),
        julian.to_jd(20 + 43, 3, 31),
        julian.to_jd(20 + 44, 4, 18),
    ]
    return y, s


def thing(dat):
    pve = ephem.previous_vernal_equinox(dat - DUBLIN_EPOCH) + DUBLIN_EPOCH
    pnm = ephem.previous_new_moon(dat - DUBLIN_EPOCH) + DUBLIN_EPOCH
    jul = julian.from_jd(dat)
    print _metonic_number(jul[0]), jul, 'days since pve:', int(dat - pve), 'days since pnm:', utils.floor(dat - pnm), _fromjd_proleptic(dat, -data.NABONASSAR_EPOCH)

print 'first day of year ... previous vernal equinox'

yearstarts, lateseleucid = define_counts()
# for date in yearstarts:
#     thing(date)

# for date in lateseleucid:
#     thing(date)

for day in range(1743763, 1743762 + 35):
    thing(day + 0.5)

# import csv

# with open('data/parker-dubberstein.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     years = []
#     for row in reader:
#         year = int(row['BC'])
#         month, day = row['1'].split('/')
#         firstday = julian.to_jd(year, int(month), int(day))

#         years.append(firstday)

# years.sort()

# for firstday in years:
#     thing(firstday)


def count_months_before_ve(ephemdate):
    moondate = ephemdate
    nve = ephem.next_vernal_equinox(moondate)
    count = 1

    while moondate < nve:
        try:
            moondate = _next_new_rising_babylon(moondate)
        except (ephem.NeverUpError, ephem.AlwaysUpError):
            moondate = ephem.next_new_moon(moondate)

        count += 1

    firstdaynextyear = moondate
    count = count - 1

    return count, firstdaynextyear

# (45, 4, 8) is first day of SE 356
# Has a metonic #: 13
print 'count of months'
end_of_era = ephem.date('/'.join(repr(x) for x in (45, 4, 8)) + ' 12:00:00')


def metonic_pattern(nextyear):
    metonic_pocket = {}

    for x in range(0, 995):

        year = ephem.localtime(nextyear).year
        m, nextyear = count_months_before_ve(nextyear)

        mstart = _metonic_start(year)

        if mstart not in metonic_pocket:
            metonic_pocket[mstart] = 0

        metonic_pocket[mstart] += m

    return metonic_pocket

# metonic_pocket = metonic_pattern(end_of_era)
# for line in metonic_pocket:
#     if metonic_pocket[line] != 235:
#         print line, metonic_pocket[line]

# count 19 years AND count 235 months. Compare how many days apart you are..
from copy import copy


def count_pattern(startingve):
    # days until ve.
    ve = copy(startingve)
    nnm = copy(startingve)

    metonic = {}

    for x in range(19):
        ve = ephem.next_vernal_equinox(ve)
        metonic[ve] = []

        while nnm < ve - 30:
            nnm = ephem.next_new_moon(nnm)
            metonic[ve].append(ephem.date(nnm))

    for m, l in metonic.items():
        print '{0}/{1}: {2}'.format(
            ephem.localtime(m).year,
            ephem.localtime(m).month,
            len(l)
        )

    print 'months', sum(len(l) for l in metonic.values())

# start = ephem.next_vernal_equinox(end_of_era)
print '///////'
# count_pattern(start)

print '------'
print 'regnal:', regnalyear(-317)
print '------'
print 'proleptic'
print _fromjd_proleptic(2456877.5 - 13, -data.NABONASSAR_EPOCH)
print _fromjd_proleptic(2456876.99, -data.NABONASSAR_EPOCH)
print 'vernal equinox\n', from_jd(2456371.5 + 1, -data.NABONASSAR_EPOCH)

print '------'

print julian.from_jd(1736016)
print from_jd(1736016)
print '------'
print julian.from_jd(1579075)
print from_jd(1579075)
