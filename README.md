# Robot Orchestra v3

A network of instrument-bashing robots.

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
