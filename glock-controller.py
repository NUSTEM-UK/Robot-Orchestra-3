"""Glockenspiel controller -- taking RTTTL requests from glock-requests.

Elements drawn from Pimoroni Piano HAT code:
https://github.com/pimoroni/Piano-HAT/blob/master/examples/simple-piano.py

Parses RTTTL, commands the rest of the system, and handles servo playback
using pigpiod for better PWM handling on Pi. Need to ensure:

  sudo pigpiod

...before running.

Python3 (log2 pre-installed rather than loaded from math module)

Dependencies (all `pip3 install`):
    pygame
    paho-mqtt

Other dependencies:
    curl -sS get.pimoroni.com/displayotron | bash
    
"""

import pygame
from time import sleep
from sys import exit
from math import ceil
#from math import log2, pow # Python3 has a log2 built-in
from math import log, pow
import numpy as np
import paho.mqtt.client as mqtt
import dothat.backlight as backlight
import dothat.lcd as lcd
from mod_orchestra import message # Network functions
from mod_audio import freq_to_note, handle_note
from rtttl import RTTTL
from rttllist import songdict
from gpiozero import Device, servo
from gpiozero.pins.pigpio import PiGPIOFactory

# Configure audio and sound synthesis.

octave = 0
octaves = 0

# Display-o-Tron setup
lcd.clear()
backlight.sweep(5)          # Set a rainbow background
lcd.set_contrast(50)        # Readable contrast, for our Displayotron HAT
lcd.write("SYSTEM START")   
backlight.graph_off()       # Make sure the hellish-bright sidebar LEDs are off

maxbpm = 160.0

# Default to pigpio pin factory, for hardware PWM
# (allows more servos to be controlled)
Device.pin_factory = PiGPIOFactory()

myservo = [Servo(27), Servo(22), Servo(5), Servo(6),
           Servo(13), Servo(19), Servo(26), Servo(21)]

def on_connect(self, client, userdata, rc):
    """Connect to MQTT broker & subscribe to cue channel."""
    print("Connected with result code: " + str(rc))
    # Subscribe to command channels
    self.subscribe("orchestra/cue")
    self.subscribe("orchestra/song")


def play_cue(cue):
    """Playback time!"""

    lcd.set_cursor_position(0,0)
    lcd.write("Now playing:".ljust(16))

    """Handle incoming playback cue."""
    notedict = {"C":36, "C#":37, "D":38, "D#":39, "E":40, "F":41, "F#":42, "G":43, "G#":44, "A":45, "A#":46, "B":47}
    channeldict = {"C":0, "C#":0, "D":1, "D#":1, "E":2, "F":3, "F#":3, "G":4, "G#":4, "A":5, "A#":5, "B":6}
    
    tune = RTTTL(cue)

    # tune is now an object storing a sequence of note frequencies and durations.
    # Iterate through that and handle each note to play back the song:

    # First extract the bpm and send that data over the network.
    message("bpm", tune.bpm)
    sleep(0.2) # Give the orchestra controller chance to think about that and stop what it's doing

    # Send the lead-in command
    message("status", "lead-in")

    # Play the lead-in. Assume we're in 4/4, because all music is, right?
    # First calculate the bpm we're actually going to use.
    divider = ceil(tune.bpm / maxbpm)
    playbpm = float(tune.bpm) / divider
    playdelay = 60.0 / playbpm

    for _ in range(4):
        myservo[7].mid()
        sleep(playdelay/4)
        myservo[7].min()
        sleep(playdelay * 3 / 4)

    # ...and away we go!
    for freq, msec in tune.notes():        
        # print(freq, msec)
        if freq != 0.0:
            note, oct = freq_to_note(freq) # Get note name and octave number from the frequency.
            print(note, oct)
            # Command the appropriate servo to move
            myservo[channeldict[note]].mid()
            # Direct audio synthesis, for testing.
            handle_note(notedict[note], oct) # Synthesise note via pygame for direct playback
            
            # Below commented out from MQTT-passing version of this (now integrated)
            # play_beats = list("00000000") # fresh playlist. List so mutable.
            # # Set the glockenspiel channel from the note name. Wrap around octaves since we only have 1 physically.
            # play_beats[channeldict[note]] = "1" 
            # playset(''.join(play_beats)) # Command the glockenspiel over MQTT
            
            sleep(0.1) # Pause for 100msec so the servo can move
            myservo[channeldict[note]].min() # Return servo to rest
            sleep((msec/1000.0) - 0.1) # Pause for the note duration, minus the default pause
        else:
            print('Rest!')
            sleep(msec/1000.0) # Pause for the rest duration (note frequency is zero).

    # Make sure the last note plays
    sleep(0.3)
    print(">>> Playback complete!")

    # Message the system to assert end of playback
    message("status", "finished")

    # reset the Display-o-Tron HAT
    lcd.clear()
    lcd.set_cursor_position(0,0)
    lcd.write("POISED READY")


def on_message(client, userdata, msg):
    """Handle incoming messages."""
    # print("Topic:", msg.topic + '  :  Message: ' + msg.payload)
    print(str(msg.topic), str(msg.payload))
    
    if str(msg.topic) == "orchestra/cue":
        """Fire the cue playback function."""
        play_cue(msg.payload)

    elif str(msg.topic) == "orchestra/song":
        print("Song title received")
        # Display song title on the HAT
        lcd.set_cursor_position(0,1)
        lcd.write(str(msg.payload[:16]).ljust(16))

    else:
        print("Well, that didn't work")


# Set up MQTT callbacks
mqttc = mqtt.Client()
mqtt_server = "10.0.1.3"
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Instantiate MQTT listener and connect
mqttc.connect(mqtt_server, 1883)

# Keep listening
mqttc.loop_forever()
