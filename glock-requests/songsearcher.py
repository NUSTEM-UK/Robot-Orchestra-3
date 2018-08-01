from rttllist import *
from bigrtttl import *
# dependency pip3 install fuzzywuzzy
# pip3 install python-Levenshtein - not dependent but removes an annoying warning
# fuzzywuzzy does our matching
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