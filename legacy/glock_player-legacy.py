"""Listen for playset messages over MQTT, and route them out to servos.

See PinFactory documentation here: 
http://gpiozero.readthedocs.io/en/stable/api_pins.html#changing-the-pin-factory

Using pigpio for better PWM handling (drives more servos).
** Need to ensure pigpiod us running: `sudo pigpiod` before running this **
"""
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
from time import sleep
from gpiozero import Device, Servo
from gpiozero.pins.pigpio import PiGPIOFactory

# Default to pigpio pin factory, for hardware PWM
# (allows more servos to be controlled)
Device.pin_factory = PiGPIOFactory()

myservo = [Servo(27), Servo(22), Servo(5), Servo(6),
           Servo(13), Servo(19), Servo(26), Servo(21)]


def on_connect(self, client, userdata, rc):
    """Connect to MQTT broker & subscribe to glock channel."""
    print("Connected with result code: " + str(rc))
    self.subscribe("orchestra/glock")


def on_message(client, userdata, msg):
    """Handle incoming beat sets on the glock channel.
    
    Timing is handled by `controller-ringtone` decoding the RTTTL sequence
    """
    # print("Topic:", msg.topic + '  :  Message: ' + msg.payload)
    print(msg.topic, msg.payload.decode('utf-8'))
    

    for i, beat in enumerate(msg.payload.decode('utf-8')):
        # print(i, beat)
        if beat == "1":
            print(i, ": BONG!")
            myservo[i].mid()
            # FIXME: Notes don't play simultaneously, because of this sleep
            # (not an issue for RTTTL monophonic tunes, but will be when
            # we get more advanced.)
            # UPDATE: Might now be fixed with out-of-loop code and
            # nested return-to-start
            #sleep(0.1)
            #myservo[i].min()
        else:
            print(i, ": PISH!")
            myservo[i].min()
    
    # Give the servos time to move as commanded
    sleep(0.1)
    
    # ...and now return the servos to rest positions
    for i in range(8):     
        myservo[i].min()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('10.0.1.3', 1883)
# client.connect('127.0.0.1', 1883)
client.loop_forever()
