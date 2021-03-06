""" Use an Adafruit Trellis array (HELLA UNTZtrument) to control the
    Robot Ochestra.

    By Jonathan Sanderson for NUSTEM, Northumbria University, UK.
    Initial version: June 2017.
    This version for Robot Orchestra v3: August 2018

    Based in part on Adafruit Trellis example code:
    Written by Limor Fried/Ladyada for Adafruit Industries.
    Python port created by Tony DiCola (tony@tonydicola.com).

    Requires Adafruit Python GPIO libraries:
    https://github.com/adafruit/Adafruit_Python_GPIO
"""

import time
from threading import Timer
from time import sleep
import Adafruit_Trellis
import numpy as np
import paho.mqtt.client as mqtt
from math import ceil
from mod_orchestra import playset, twitch, message
from gpiozero import Button

# Global variables. Which is nasty, right?
currentBeat = 0  # Keep track of which beat we're playing.

defaultBPM = 120 # Barfs if we go much above 120; playBeat doesn't complete before next call. Eek!
bpm = defaultBPM
tempo = 60.0 / defaultBPM
maxbpm = 160.0
startStopButton = Button(5, pull_up=True, bounce_time=0.3)
running = True


class RepeatedTimer(object):
    """Simple timer class, from StackExchange (obviously).

    Credit: user MestreLion, https://stackoverflow.com/questions/3393612

    Modified to allow change of interval without tearing down the timer.
    """

    def __init__(self, interval, function, *args):
        """Initialize the timer object."""
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.is_running = False
        self.start()

    def _run(self):
        """Timer has been triggered: execute callback function."""
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        """Start the timer, if it's not already running."""
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """Stop the timer."""
        self._timer.cancel()
        self.is_running = False

    def bpm(self, newBPM):
        """Reset the interval to new beats per minute."""
        self.interval = (60/newBPM)


# BEGIN Trellis initialisation
matrix0 = Adafruit_Trellis.Adafruit_Trellis()
matrix1 = Adafruit_Trellis.Adafruit_Trellis()
matrix2 = Adafruit_Trellis.Adafruit_Trellis()
matrix3 = Adafruit_Trellis.Adafruit_Trellis()
matrix4 = Adafruit_Trellis.Adafruit_Trellis()
matrix5 = Adafruit_Trellis.Adafruit_Trellis()
matrix6 = Adafruit_Trellis.Adafruit_Trellis()
matrix7 = Adafruit_Trellis.Adafruit_Trellis()

trellis = Adafruit_Trellis.Adafruit_TrellisSet(matrix0, matrix1, matrix2,
                                               matrix3, matrix4, matrix5,
                                               matrix6, matrix7)

# set to however many you're working with here, up to 8 per I2C bus
NUMTRELLIS = 8
numKeys = NUMTRELLIS * 16

# Connect Trellis Vin to 5V and Ground to ground.
# Connect Trellis INT wire to a digital input (optional)
# Connect Trellis I2C SDA pin to your board's SDA line
# Connect Trellis I2C SCL pin to your board's SCL line
# All Trellises on an I2C bus share the SDA, SCL and INT pin!
# Even 8 tiles use only 3 wires max

# Set this to the number of the I2C bus that the Trellises are attached to:
I2C_BUS = 1

# Setup
print('Trellis Active')

# begin() with the I2C addresses and bus numbers of each panel in order
trellis.begin((0x70, I2C_BUS), (0x71, I2C_BUS), (0x72, I2C_BUS),
              (0x73, I2C_BUS), (0x74, I2C_BUS), (0x75, I2C_BUS),
              (0x76, I2C_BUS), (0x77, I2C_BUS))

# END Trellis initialisation


# It's ridiculous to pull in all of Numpy just to do a two-dimensional
# array, but apparently that's what I'm doing.
# Also: yes, I typed this out by hand.
buttonGrid = np.array(
                      [[  0,   1,   2,   3,  16,  17,  18,  19,  32,  33,  34,  35,  48,  49,  50,  51],
                       [  4,   5,   6,   7,  20,  21,  22,  23,  36,  37,  38,  39,  52,  53,  54,  55],
                       [  8,   9,  10,  11,  24,  25,  26,  27,  40,  41,  42,  43,  56,  57,  58,  59],
                       [ 12,  13,  14,  15,  28,  29,  30,  31,  44,  45,  46,  47,  60,  61,  62,  63],
                       [ 64,  65,  66,  67,  80,  81,  82,  83,  96,  97,  98,  99, 112, 113, 114, 115],
                       [ 68 , 69,  70,  71,  84,  85,  86,  87, 100, 101, 102, 103, 116, 117, 118, 119],
                       [ 72,  73,  74,  75,  88,  89,  90,  91, 104, 105, 106, 107, 120, 121, 122, 123],
                       [ 76,  77,  78,  79,  92,  93,  94,  95, 108, 109, 110, 111, 124, 125, 126, 127]]
                     )

# Helpful hardware test routine: animate all the LEDs on, then off again.
# Removed for startup performance, but left in place for testing purposees.
# for row in range(8):
#     for column in range(16):
#         trellis.setLED(buttonGrid[row, column])
#         trellis.writeDisplay()
#         time.sleep(0.01)
#
# for row in range(8):
#     for column in range(16):
#         trellis.clrLED(buttonGrid[row, column])
#         trellis.writeDisplay()
#         time.sleep(0.01)


# Let's get some MQTT action going
def on_connect(self, client, userdata, rc):
    """Connect to the MQTT broker and subscribe to relevant channels."""
    print("Connected with result code: " + str(rc))
    self.subscribe("orchestra/status")
    self.subscribe("orchestra/bpm")

def on_message(client, userdata, msg):
    """Handle incoming MQTT message."""
    global currentBeat
    global bpm
    global defaultBPM
    global running

    msg.payload = msg.payload.decode("utf-8") # Because it's bytes on the wire. Ugh.
    print(str(msg.topic), str(msg.payload))

    if str(msg.topic) == "orchestra/bpm":
        """Prepare for playback."""
        print(">>> BPM UPDATE!")
        print(str(msg.topic), int(msg.payload))
        rt.stop() # Stop playback
        running = False # Semaphore the rest of the system
        # We need to handle insanely high bpm settings, since the dataset includes some
        # (presumably for temporal resolution reasons in the song playback. Ah, high fidelity)
        # The maximum bpm the Trellis can handle is about 160, so:
        divider = ceil(float(msg.payload)/maxbpm) # Get the divider with which we'll need to work
        bpm = float(msg.payload) / divider
        # bpm = int(msg.payload)
        rt.bpm(bpm)


    elif str(msg.topic) == "orchestra/status":
        """Handle playback status updates related to glockenspiel requests.
        
        Doing it all this way is a bit of a legacy of how I'd originally planned to 
        have a conducting instrument as a separate thing. In practice, we used servo #7 
        on the glockenspiel as an expedient alternative - it plays a bar of lead-in, then
        the orchestra and melody are cued. The lead-in helps differentiate 'normal'
        orchestra playback, and glockenspiel-accompanyment playback.

        This pathway is never triggered if the glockenspiel requests front-end is not
        running.
        """
        if str(msg.payload) == "lead-in":
            print(">>> LEAD-IN!")
            currentBeat = 0 # Rewind to the start of the Trellis
            rt.bpm(bpm) # Set new tempo. TODO: sanity check!
            print(">>> LEAD-IN PLAYING", bpm)
            delay = 60.0/bpm
            # Pause for lead-in count
            sleep(delay * 3)
            rt.start()  # Restart the Trellis playback
            running = True
            print(">>> PLAY BACKING TRACK")
    
        elif str(msg.payload) == "finished":
            print(">>> FINISHED!")
            rt.stop()   # Stop playback
            running = False
            bpm = defaultBPM
            rt.bpm(bpm) # Reset Orchestra tempo
    
    else:
        print("MQTT error.")


def playBeat():
    # We're using currentBeat and curState from the global namespace,
    # which I now think isn't what the `global` keyword means. Whoops.
    global currentBeat

    # Make ourselves an empty array in which we'll hold this column of beats
    curState = np.array([0, 0, 0, 0, 0, 0, 0, 0])

    target = buttonGrid[0, currentBeat]

    # Get current state of this column of buttons
    for row in range(8):
        curState[row] = trellis.isLED(buttonGrid[row, currentBeat])

    # Concatenate array into string, for MQTT sending
    # array2string adds square braces; slice to remove them.
    curStateString = np.array2string(curState, separator='')[1:-1]
    # print curStateString

    # flash column header
    # It's rather too slow to flash the whole column, which is what I wanted,
    # so this will have to do. Boo!
    # Note that the animation here is visually different based on the
    # current state of the column. Hence timing across the board doesn't
    # look smooth. I should probably test the current state and amend
    # the flash animation based on the result. But then... would the two
    # code paths actually take the same period of time?
    trellis.clrLED(target)
    trellis.writeDisplay()
    trellis.setLED(target)
    trellis.writeDisplay()

    # Return column to previous state
    if curState[0] == 1:
        trellis.setLED(target)
    else:
        trellis.clrLED(target)

    # Command the orchestra!
    playset(curStateString)
    # ...and update the display
    trellis.writeDisplay()

    # set up for next beat, looping when we reach the end.
    currentBeat += 1
    if currentBeat > 15:
        currentBeat = 0


# ...and now we can actually run some code.
print('Press Ctrl-C to quit.')

# Reset the Trellis array
trellis.clear()
trellis.writeDisplay()

# Initialise the timer, which will trigger at a rate specified by the
# bpm setting. Note that the timer is not running when instantiated.
rt = RepeatedTimer(tempo, playBeat)

# Set up MQTT connection and callback handling
mqttc = mqtt.Client()
mqtt_server = "10.0.1.3"
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(mqtt_server, 1883)

mqttc.loop_start()

# ...so we finally get to the main loop.

# The main loop needs to handle button presses and MQTT update callbacks
# ...which are blocking. And we have a global callback thread timer running.
# Sheesh, flow control in this code is gnarly.
try:
    while True:
        time.sleep(0.08) # TODO: Replace with MQTT check.

        # If a button was just pressed or released...
        if trellis.readSwitches():
            # go through every button
            for i in range(numKeys):
                # if it was pressed...
                if trellis.justPressed(i):
                    print('Button: {0}'.format(i))
                    # Alternate the LED
                    if trellis.isLED(i):
                        trellis.clrLED(i)
                    else:
                        trellis.setLED(i)
            # Update Trellis display.
            # Disabled by default since this gets triggered by the
            # timer anyway, and too frequent writeDisplays tend to
            # send things a bit funky.
            # trellis.writeDisplay()
        if startStopButton.is_pressed:
            if running:
                # Stop playback!
                print('>>> STOP')
                rt.stop()
                running = False
            else:
                # Start playback!
                # This will also trigger playback on first launch, since startStopButton.is_pressed is false,
                # so we fall through to this path. Which wasn't how I'd planned to do things, but achieves the
                # outcome I'd intended. Schrödinger's bug?
                print('>>> START', bpm)
                rt.start()
                running = True
finally:
    rt.stop()
    mqttc.loop_stop()
