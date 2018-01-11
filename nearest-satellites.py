#!/usr/bin/env python
import ephem
from datetime import datetime, timedelta
from math import cos, sqrt
from operator import itemgetter
import sys

refbodyname = '0 ISS (ZARYA)'
startdelta = timedelta(90)
enddelta = timedelta(180)
starttime = datetime.utcnow() - startdelta
numdays = 1
resolution = 60 # seconds

bodies = []
refbody = ''

with open('tle.txt') as f:
    l0 = ''
    l1 = ''
    l2 = ''
    body = ''
    for line in f:
        line = line.strip()
        if line.startswith('0'):
            l0 = line
        elif line.startswith('1'):
            l1 = line
        elif line.startswith('2'):
            if 'SOYUZ' in l0 or 'PROGRESS' in l0:
                break
            l2 = line
            body = ephem.readtle(l0, l1, l2)
            if l0 == refbodyname:
                refbody = body
            else:
                bodies.append(body)

endtime = starttime + enddelta
resdelta = timedelta(seconds = resolution)
curtime = starttime

nearests = []

while curtime <= endtime:
    curtimes = curtime.strftime('%Y/%m/%d %H:%M:%S')
    print('== processing ' + curtimes)

    observer = ephem.Observer()
    observer.lon = 0
    observer.lat = 0
    observer.elevation = -6371000 # center of the earth
    observer.date = curtimes

    refbody.compute(observer)
    # distances = []
    nearestdistance = 99999999999999999999999999999
    nearestname = ''

    for body in bodies:
        try:
            body.compute(observer)
            angle = float(repr(ephem.separation(refbody, body)))
            a = refbody.range
            b = body.range
            # print(separation, range1, range2)
            distance = sqrt(a**2 + b**2 - 2*a*b*cos(angle))
            # distances.append([body.name, distance])
            if distance < nearestdistance:
                nearestdistance = distance
                nearestname = body.name
        except:
            pass

    print(nearestdistance, nearestname)
    nearests.append([nearestdistance, nearestname, curtimes])
    curtime += resdelta

nearests.sort(key=itemgetter(0), reverse=True)
uniquenearest = {}

for distance in nearests:
    uniquenearest[distance[1]] = distance[0]

sumdistance = ndistance = 0
for distance in nearests:
    sumdistance += distance[0]
    ndistance += 1
averagedistance = sumdistance / ndistance

print('===== average minimum distance to nearest satellite: ', averagedistance)
print('===== total satellites: ', len(bodies))
print('===== list of close by satellites:')

i=0
for key, value in sorted(uniquenearest.items(), key=lambda item: (item[1],item[0])):
    print("%s: %s" % (value, key))
    i += 1
    if i>100:
        break

