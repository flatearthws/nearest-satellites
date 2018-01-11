nearest-satellites.py - Calculating The Nearest Satellite From the ISS
======================================================================

This script calculates the nearest satellites from the ISS. It iterates
every minute between -3 to +3 months from now, and calculate the
nearest satellite at the given minute. At the end it tabulates the results
and displays the 100 nearest satellites from the ISS, as well as their
distances and the average distance.

This is intended to show that it is unrealistic to expect satellites to appear in photos taken from the ISS. We can't rule out the possibility of satellites appearing in ISS photos, but it would be an extraordinary event, at least when using wide angle lenses usually used to take pictures from the ISS.

## Usage

* Install python and [pyephem](http://rhodesmill.org/pyephem/)
* Put satellite TLE data in tle.txt. Get the TLE data from sites like [Space Track](https://www.space-track.org/). You need a fresh TLE data because the script uses current time.
* Run `nearest-satellites.py` and wait for several hours.

## Credits

The script is created for the [BumiDatar.id](https://bumidatar.id) and [FlatEarth.ws](https://flatearth.ws) projects, debunking flat Earth misconceptions.