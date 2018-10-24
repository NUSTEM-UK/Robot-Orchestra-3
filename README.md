# Robot Orchestra v3

A network of instrument-bashing robots. This version has the following features:

* Supports ESP8266 orchestra robots, commanded over MQTT on local wifi. 8 channels are switchable at runtime by grounding pins D5,6,7 to earth as a binary channel identifier.
* Python-based orchestra controller running on a Pi host, using an Adafruit Hella UNTZtrument button controller board as a physical sequencer. The controller script outputs beat patterns over MQTT.
* MQTT command pattern is a string (!) of eight 1/0 signals, per beat. Yes, this is terrible... but it's also terribly simple.
* Separate glockenspiel controller listens for MQTT packages containing RTTTL ringtone code strings, then cues playback for itself and the orchestra robots. The physical glockenspiel was a copper pipe instrument with servo-actuated hammers; a full octave running off a single Raspberry Pi. Python script.
* A requests controller (Pi/Python) takes song requests at the console, sloppy matches input strings against a library of approx. 10k 1990s-vintage mobile phone ringtones, and sends the best match (however bad that might be) to the glockenspiel.

Other components (in earlier repositories, because they're maybe still relevant) included a software version of the UNTZtrument, coded in Python GUIZero.

## Current status

The specific glockenspiel this release was developed to drive did not survive a hectic weekend of use at the Great Exhibition of the North Family Expo, summer 2018. It was retired / recycled subsequently. Hence, we currently have a controller with nothing to control. Sniff.

### General configuration

Every Pi in the system will need:

    pip3 install paho-mqtt


### glock_player

Python-based player clinet for Raspberry Pi GPIO. Uses GPIOZero, with `pigpio`-based output for better servo performance (can handle at least 8 servos in software). Used to drive glockenspiel: fairly dumb script, command and controll is handler by `controller-ringtone`

### glock-controller


### orchestra-controller

Needs Adafruit GPIO installed:

    git clone https://github.com/tdicola/Adafruit_Trellis_Python
    cd Adafruit_Trellis_Python
    sudo python setup.py install
    pip3 install adafruit-gpio


## Sequence of operation

### Bring up network

### Bring up MQTT broker on 10.0.1.3

It's worth running the following on that box to diagnose network traffic:

    mosquitto_sub -v -t orchestra/+

Note that you can send test or debug messages using something like:

    mosquitto_pub -h 10.0.1.3 -t orchestra/bpm -m 140
