import numpy as numpy
import matplotlib.pyplot as plt

from bigrtttl import *
from rtttl import RTTTL

data = []

for key, value in songdictEgg.items():
    song = RTTTL(value)
    # print(key, song.bpm) # Used for debugging malformed RTTTL lines
    if song.bpm > 500:
        print(key, song.bpm)
    else:
        data.append(song.bpm)

plt.hist(data, bins=50)
plt.show()