# Robot Orchestra v3

A network of instrument-bashing robots.

### glock_player

Python-based player clinet for Raspberry Pi GPIO. Uses GPIOZero, with `pigpio`-based output for better servo performance (can handle at least 8 servos in software). Used to drive glockenspiel: fairly dumb script, command and controll is handler by `controller-ringtone`

### glock-controller




## Sequence of operation

### Bring up network

### Bring up MQTT broker on 10.0.1.3

It's worth running the following on that box to diagnose network traffic:

    mosquitto_sub -v -t orchestra/+



