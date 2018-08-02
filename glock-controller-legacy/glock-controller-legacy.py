"""Robot Orchestra controller - taking RTTTL ringtone requests from Twitter.

Elements drawn from Pimoroni Piano HAT code:
https://github.com/pimoroni/Piano-HAT/blob/master/examples/simple-piano.py

Python3 (log2 pre-installed rather than loaded from math module)

Dependencies (all `pip3 install`):
    pygame
    paho-mqtt
    dothat
"""

import glob
import os
import re
import pygame
from time import sleep
from sys import exit
from rtttl import RTTTL
from rttllist import songdict
from threading import Timer
import paho.mqtt.client as mqtt
import numpy as np
# from math import log2, pow # Python3 has a log2
from math import log, pow
# Uses Pimoroni Display-o-Tron HAT for on-Pi status display
import dothat.backlight as backlight
import dothat.lcd as lcd

try:
    pygame.init() # Throws error in pylint: security issue for C module. Ignore.
except ImportError:
    exit("This script requires the pygame module\nInstall with: sudo pip3 install pygame")

BANK = os.path.join(os.path.dirname(__file__), "sounds")

NOTE_OFFSET = 0
FILETYPES = ['*.wav', '*.ogg']
samples = []
files = []
octave = 0
octaves = 0

# Tuning, and constants for freq-to-note conversion
A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

mqttc = mqtt.Client()
# mqtt_server = "127.0.0.1"
mqtt_server = "10.0.1.3"


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(256)

patches = glob.glob(os.path.join(BANK, '*'))
print(patches)
patch_index = 0

if len(patches) == 0:
    exit("Couldn't find any .wav files in {}".format(BANK))

# Display-o-Tron setup
lcd.clear()
backlight.sweep(5)          # Set a rainbow background
lcd.set_contrast(50)        # Readable contrast, for our Displayotron HAT
lcd.write("SYSTEM START")   
backlight.graph_off()       # Make sure the hellish-bright sidebar LEDs are off


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]


def load_samples(patch):
    """Load audio samples into buffers for playback."""
    global samples, files, octave, octaves
    files = []
    print('Loading samples from: {}'.format(patch))
    for filetype in FILETYPES:
        files.extend(glob.glob(os.path.join(patch, filetype)))
    files.sort(key=natural_sort_key)
    octaves = len(files) / 12
    samples = [pygame.mixer.Sound(sample) for sample in files]
    octave = int(octaves / 2)


def handle_note(channel, octave):
    """Synthesise a commanded note using Pygame samples: direct audio playback."""
    channel = channel + (12 * octave) + NOTE_OFFSET
    if channel < len(samples):
        # print('Playing Sound: {}'.format(files[channel]))
        print('Playing sound: {}'.format(channel))
        samples[channel].play(loops=0)
    else:
        print('Note out of bounds')


def handle_octave_up():
    global octave
    if octave < octaves:
        octave += 1
        print('Selected Octave: {}'.format(octave))


def handle_octave_down():
    global octave
    if octave > 0:
        octave -= 1
        print('Selected Octave: {}'.format(octave))


def scale_up(notes, delay):
    global octave
    for note in range(notes):
        handle_note(note, octave)
        sleep(delay)


def scale_down(notes, delay):
    global octave
    for note in range(notes):
        handle_note(notes-note, octave)
        sleep(delay)


def freq_to_note(freq):
    """Outputs note and octave for input frequency.

    Based on https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/
    by John D. Cook
    """
    # h = round(12*log2(freq/C0)) # Python3 only
    h = round(12*(log(freq/C0)/log(2)))
    octave = (h // 12) - 6
    n = h % 12
    return name[int(n)], int(octave)

def on_connect(self, client, userdata, rc):
    """Connect to MQTT broker & subscribe to cue channel."""
    print("Connected with result code: " + str(rc))
    # Subscribe to command channels
    self.subscribe("orchestra/cue")
    self.subscribe("orchestra/song")
    self.subscribe("orchestra/handle")

def message(topic, payload):
    """Abstract out MQTT connection.

    Since it has to be done for each message, wrap it in a function.
    """
    mqttc.connect(mqtt_server, 1883)
    mqttc.publish("orchestra/" + topic, payload)

def playset(beatset):
    """Sends the current note to all 8 channels at once."""
    message("glock", beatset)

def on_message(client, userdata, msg):
    """Handle incoming messages."""
    # print("Topic:", msg.topic + '  :  Message: ' + msg.payload)
    print(str(msg.topic), str(msg.payload))
    
    if str(msg.topic) == "orchestra/cue":
        """Handle RTTTL song cue command."""
        lcd.set_cursor_position(0,0)
        lcd.write("Now playing:".ljust(16))

        """Handle incoming playback cue."""
        notedict = {"C":36, "C#":37, "D":38, "D#":39, "E":40, "F":41, "F#":42, "G":43, "G#":44, "A":45, "A#":46, "B":47}
        channeldict = {"C":0, "C#":0, "D":1, "D#":1, "E":2, "F":3, "F#":3, "G":4, "G#":4, "A":5, "A#":5, "B":6}
        
        tune = RTTTL(msg.payload)

        # tune is now an object storing a sequence of note frequencies and durations.
        # Iterate through that and handle each note to play back the song:

        for freq, msec in tune.notes():        
            # print(freq, msec)
            if freq != 0.0:
                note, oct = freq_to_note(freq) # Get note name and octave number from the frequency.
                print(note, oct)
                play_beats = list("00000000") # fresh playlist. List so mutable.
                # Set the glockenspiel channel from the note name. Wrap around octaves since we only have 1 physically.
                play_beats[channeldict[note]] = "1" 
                playset(''.join(play_beats)) # Command the glockenspiel over MQTT
                handle_note(notedict[note], oct) # Synthesise note via pygame for direct playback
                sleep(msec/1000.0) # Pause for the note duration.
            else:
                print('Rest!')
                sleep(msec/1000.0) # Pause for the rest duration (note frequency is zero).

        # Make sure the last note plays
        sleep(0.3)
        print(">>> Playback complete!")
        lcd.clear()
        lcd.set_cursor_position(0,0)
        lcd.write("POISED READY")

    elif str(msg.topic) == "orchestra/song":
        print("Song title received")
        # Display song title on the HAT
        lcd.set_cursor_position(0,1)
        lcd.write(str(msg.payload[:16]).ljust(16))

    elif str(msg.topic) == "orchestra/handle":
        lcd.set_cursor_position(0,2)
        # Display song requester
        lcd.write("For: " + str(msg.payload[:11]).ljust(11))
   
    else:
        print("Well, that didn't work")


# Now we can set up the environment and instantiate handlers

# Load audio samples
load_samples(patches[patch_index])

# Set up MQTT listener
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Instantiate MQTT listener and connect
client.connect(mqtt_server, 1883)

# Keep listening
client.loop_forever()
