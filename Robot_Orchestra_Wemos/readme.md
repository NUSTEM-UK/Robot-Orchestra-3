# Robot Orchestra - Huzzah version

This version of the workshop uses a simplified circuit based on Adafruit Huzzah devices, in place of the original Arduino Uno-based system.

## Advantages
* Synchronised playback of all instruments assembled during session.
* Leverages key Internet of Things technologies, facilitating discussion of issues surrounding pervasive networking.
* Simpler programming, based around Python rather than Arduino code, with beat patterns deliverable via text files over the network rather than requiring the Arduino to be re-flashed from C code.

## Function

`instruments.py` stores a dictionary of robot identifier strings (based on hardware MAC addresses) and the human-readable ID number. Which is written on the modules in Sharpie, obviously.

`mod_orchestra.py` wraps the MQTT-based messaging in helper functions. There are two modes of operation:

* Approach 1:
    * send `twitch` to list of robots in use (default: ALL)
    * example: `twitch.py`.
    * Useful during construction and while debugging. All robots under construction will twitch in sync, and since the activate string is sent for each twitch, robots hopping on and off the network will twitch within a few seconds of being powered up.
* Approach 2:
    * distribute playback strings to individual robots.
    * Cue playback of stored strings by all robots.
    * Example: `robot_orchestra.py`.
    * Useful for scripting song playback / more interesting patterns across completed instruments.

Occasionally, Huzzahs seem to get stuck and refuse to command a servo to deflect more than a couple of degrees. Swapping from `twitch.py` to `robot_orchestra.py` seems to fix it. As of 2017-02-08... I've no idea what's going on.


## ToDo

* Write a more sane initialiser for the robots, so the list doesn't need to be in three places.
* Modify `robot_orchestra.py` to accept input files, rather than have filename hard-coded.
* Write patchboard grammar (and possible UI) to assign individual robots to groups. Helper functions currently cater for this (see DRUMS group: hurray for forward planning).
* Script playback from [UNTZtrument](https://www.adafruit.com/product/1999).
* Upgrade the Sharpie labels to nicely printed versions. Because the Sharpie rubs off.
