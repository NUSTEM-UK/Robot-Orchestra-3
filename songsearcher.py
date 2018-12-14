"""Fuzzy matching to a library of songs in RTTTL format.

Takes an input string and matches against song title in a dictionary of available songs. 
Returns song title, RTTTL string, and match confidence metric. Fuzzy matching applied so
a 'match' is guaranteed, however wayward the confidence.

Dependencies:
    pip3 install fuzzywuzzy
    pip3 install python-Levenshtein

(the latter doesn't seem to be strictly necessary, but removes an annoying warning at runtime.)
"""

from rttllist import *
from bigrtttl import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def searcher(input_string):
    bestGuess = []
    bestAccuracy = 0
    input_string = input_string.lower()
    
    # We're searching the full list, which was previously an easter egg in the Twitter matcher.
    # Hence the weird dictionary names here.
    for key, value in songdictEgg.items():
        accuracy = fuzz.token_set_ratio(input_string, key)
        if accuracy > bestAccuracy:
            bestGuess = key
            bestAccuracy = accuracy
            bestRTTTL = value
            
    return(bestGuess, bestAccuracy, bestRTTTL)

# if __name__ == "__main__" means this code will only run if this is the main python code (not imported as a module)
if __name__ == "__main__":
    tweet = "#nustem walking"
    a,b,c = searcher(tweet)
    print(a,b)
    print(c)