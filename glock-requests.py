""" Handle song requests from the terminal.

Take terminal input, match to RTTTL song list, send cues to glockenspiel.

Dependencies (pip3 install):
    paho-mqtt
    fuzzywuzzy (in songsearcher module)
    python-Levenshtein (in songsearcher module)
    termcolor

"""

import sys
from time import sleep
import ro_helpers_network
from termcolor import colored, cprint
from songsearcher import searcher

def welcome():
    """Output the banner title."""
    print("")
    cprint(" █▀▀█ █▀▀█ █▀▀▄ █▀▀█ ▀▀█▀▀   █▀▀█ █▀▀█ █▀▀ █░░█ █▀▀ █▀▀ ▀▀█▀▀ █▀▀█ █▀▀█", 'red')
    cprint(" █▄▄▀ █░░█ █▀▀▄ █░░█ ░░█░░   █░░█ █▄▄▀ █░░ █▀▀█ █▀▀ ▀▀█ ░░█░░ █▄▄▀ █▄▄█", 'red')
    cprint(" ▀░▀▀ ▀▀▀▀ ▀▀▀░ ▀▀▀▀ ░░▀░░   ▀▀▀▀ ▀░▀▀ ▀▀▀ ▀░░▀ ▀▀▀ ▀▀▀ ░░▀░░ ▀░▀▀ ▀░░▀", 'red')
    cprint("Bringing awful 90s ringtones into the Internet of Things era, since 2018", 'yellow')
    print("")

def get_input():
    """Collect request string from shell."""
    cprint("Request a song name: ", "green")
    return input("--> ")
    
def respond(request, song, accuracy):
    """Respond to the input request."""
    print()
    respond_string = colored("You asked for: ", 'yellow')
    respond_string += colored(request, 'green')
    cprint(respond_string)
    sleep(0.5)
    respond_string2 = colored("I'm ", 'yellow')
    respond_string2 += colored(accuracy, 'green')
    respond_string2 += colored("% confident that matches: ", 'yellow')
    respond_string2 += colored(song, 'green') 
    cprint(respond_string2)
    print()
    sleep(0.5)

def play_song(song, cue):
    """Command the glockenspiel."""
    cprint("Playing my best guess in", 'yellow')
    countdown()
    sleep(0.8)
    print()
    cprint(" █▀▀█ █░░ █▀▀█ █░░█ ░▀░ █▀▀▄ █▀▀▀", 'green')
    cprint(" █░░█ █░░ █▄▄█ █▄▄█ ▀█▀ █░░█ █░▀█", 'green')
    cprint(" █▀▀▀ ▀▀▀ ▀░░▀ ▄▄▄█ ▀▀▀ ▀░░▀ ▀▀▀▀", 'green')
    print()
    # message("orchestra/song", song)
    sleep(0.2)
    # message("orchestra/cue", cue)


def song_complete():
    print()
    cprint(" █▀▀ ░▀░ █▀▀▄ ░▀░ █▀▀ █░░█ █▀▀ █▀▀▄", 'cyan')
    cprint(" █▀▀ ▀█▀ █░░█ ▀█▀ ▀▀█ █▀▀█ █▀▀ █░░█", 'cyan')
    cprint(" ▀░░ ▀▀▀ ▀░░▀ ▀▀▀ ▀▀▀ ▀░░▀ ▀▀▀ ▀▀▀░", 'cyan')
    print()
    cprint("Thank you for your request.", 'yellow')
    print()
    sleep(0.5)
    cprint("Returning to start in:")
    sleep(0.5)
    countdown()
    clear_screen()

def clear_screen():
    for _ in range(30):
        print()
        sleep(0.05)

def countdown():
    cprint("...3", 'red')
    sleep(1)
    cprint("...2", 'magenta')
    sleep(1)
    cprint("...1", 'green')
    sleep(0.8)    

if __name__ == "__main__":
    clear_screen()
    welcome()
    request = get_input()
    # print(request)
    print()
    cprint(">>> MATCHING...", 'red')
    guessed_song_title, match_accuracy, song_rtttl = searcher(request)
    
    respond(request, guessed_song_title, match_accuracy)
    play_song(guessed_song_title, song_rtttl)
    sleep(2)
    song_complete()
    welcome()
