#!/usr/bin/env python
import ephem
from datetime import datetime, timedelta
from math import cos, sqrt
from operator import itemgetter
import statistics

# TLE file
tlefile = 'tle.txt'

# ISS name in the TLE file
refbodyname = '0 ISS (ZARYA)'

# start of analysis (90 days in the past)
starttime = datetime.utcnow() - timedelta(90)

# end of analysis (180 days after starting time)
endtime = starttime + timedelta(180)

# sampling rate
resdelta = timedelta(seconds = 60)



bodies = []
refbody = ''

with open(tlefile) as f:
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


nearests = []
curtime = starttime

while curtime <= endtime:
    curtimes = curtime.strftime('%Y/%m/%d %H:%M:%S')
    print('== processing ' + curtimes)

    observer = ephem.Observer()
    observer.lon = 0
    observer.lat = 0
    observer.elevation = -6371000 # center of the earth
    observer.date = curtimes

    refbody.compute(observer)
    nearestdistance = 99999999999999999999999999999
    nearestname = ''

    for body in bodies:
        try:
            body.compute(observer)
            angle = float(repr(ephem.separation(refbody, body)))
            a = refbody.range
            b = body.range
            distance = sqrt(a**2 + b**2 - 2*a*b*cos(angle))
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

# sumdistance = ndistance = 0
distances = []
for distance in nearests:
    distances.append(distance[0])
mean = statistics.mean(distances)
stdev = statistics.stdev(distances)
pstdev = statistics.pstdev(distances)
pvariance = statistics.pvariance(distances)
variance = statistics.variance(distances)

print()
print('RESULTS: ')
print('starttime: ', starttime)
print('endtime: ', endtime)
print('sampling rate: ', resdelta)
print('mean: ', mean)
print('stddev: ', stdev)
print('pstddev: ', pstdev)
print('variance: ', variance)
print('pvariance: ', pvariance)
print('n: ', len(distances))
print('total satellites: ', len(bodies)-1)
print('list of nearest satellites:')

i=0
for key, value in sorted(uniquenearest.items(), key=lambda item: (item[1],item[0])):
    print("%s: %s" % (value, key))
    i += 1
    if i>100:
        break

