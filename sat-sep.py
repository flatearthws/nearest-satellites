#!/usr/bin/env python
import ephem
from datetime import datetime, timedelta
from math import cos, sqrt

curtimes = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')
observer = ephem.Observer()
observer.lon = 0
observer.lat = 0
observer.elevation = -6371000 # center of the earth
observer.date = curtimes
observer.temp = -272
observer.pressure = 0

telkom = ephem.readtle(
    'TELKOM 1',
    '1 25880U 99042A   18010.09216017 -.00000146  00000-0  00000+0 0  9994',
    '2 25880   0.2775  96.2025 0025573 178.5731 309.0390  1.00245330 67469'
)

nss11 = ephem.readtle(
    'NSS 11 (AAP-1)',
    '1 26554U 00059A   18010.20786900  .00000034  00000-0  00000+0 0  9994',
    '2 26554   0.0313 299.4809 0001258 154.8148 254.6409  1.00915493 63291'
)

ses7 = ephem.readtle(
    'SES 7 (PROTOSTAR 2)',
    '1 34941U 09027A   18010.10257669 -.00000350  00000-0  00000+0 0  9993',
    '2 34941   0.0515  80.5525 0002700 204.8710 329.2922  1.00269382 31734'
)

telkom.compute(observer)
nss11.compute(observer)
ses7.compute(observer)

print('telkom', telkom.sublat, telkom.sublong, telkom.elevation)
print('nss11', nss11.sublat, nss11.sublong, nss11.elevation)
print('ses7', ses7.sublat, ses7.sublong, ses7.elevation)

a = telkom.range
b = nss11.range
angle = ephem.separation(telkom, nss11)
print('jarak telkom-nss11', sqrt(a**2 + b**2 - 2*a*b*cos(angle)))

a = telkom.range
b = ses7.range
angle = ephem.separation(telkom, ses7)
print('jarak telkom-ses7', sqrt(a**2 + b**2 - 2*a*b*cos(angle)))

a = ses7.range
b = nss11.range
angle = ephem.separation(ses7, nss11)
print('jarak ses7-nss11', sqrt(a**2 + b**2 - 2*a*b*cos(angle)))
