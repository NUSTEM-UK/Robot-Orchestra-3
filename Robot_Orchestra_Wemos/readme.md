# Robot Orchestra - Wemos version

This version of the workshop uses a simplified circuit based on Wemos D1 mini devices, in place of the original Arduino Uno-based system. An intermediate version was based on Adafruit Huzzah boards, which are functionally similar to the D1 minis -- some references may remain in the codebase and documentation.

## Advantages
* Synchronised playback of all instruments assembled during session.
* Leverages key Internet of Things technologies, facilitating discussion of issues surrounding pervasive networking.
* Simple programming, based around Python rather than Arduino code, with beat patterns deliverable via text files over the network rather than requiring the Arduino to be re-flashed from C code.
* Possibility for live playback from a sequencer-style interface (see `orchestra-controller.py`).

## Function

> As of 2018-12-14 I'm honestly not sure this is correct any more, in that I think I have each D1 listening to the same broadcast channel for an eight-character play string (look for `playset` in the `.ino` file). Each device has a runtime-changable hardware-specified channel assignment (short pins D5/6/7 to ground for a 3-bit binary channel number); it reads the corresponding character and plays either a beat or a miss accordingly. But it's now so long since I wrote this that that may only be how I *think* it works, not how it actually works. Curse these embedded controllers and their ability to sit on a shelf for a year and then work flawlessly as soon as you bung 5V across them!

> If memory serves, the 'old-style' approach documented below of sending a playback beat pattern to a specific device, then cueing playback across all the boards, remains in the code. It's just not used in the system as currently deployed. I love the smell of legacy code in the morning.

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
* Modify `robot_orchestra.py` to accept input files, rather than have filename hard-coded. (DONEish)
* Write patchboard grammar (and possible UI) to assign individual robots to groups. Helper functions currently cater for this (see DRUMS group: hurray for forward planning).
* Script playback from [UNTZtrument](https://www.adafruit.com/product/1999). (DONE)
* Upgrade the Sharpie labels to nicely printed versions. Because the Sharpie rubs off. (ALSO DONE)
