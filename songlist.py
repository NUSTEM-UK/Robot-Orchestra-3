"""Output the list of song titles from the big RTTTL list.

Used purely to generate the songlist document, later formated in Pages.
This probably shouldn't be at the root level, but I'm trying to avoid
gnarly imports or duplicates of the songlist file.
"""

from bigrtttl import *

for key, value in songdictEgg.items():
    print(key)
    