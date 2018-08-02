"""Robot orchestra abstractions.

Provides a simple language grammar for issuing beat patterns and playback
cue to Robot Orchestra instruments, and handles MQTT messaging to distribute
those commands.

Can be straightforwardly extended to simplify grammar, which we leave as an
exercise for workshop participants.

Requires `sudo pip install paho-mqtt` on a vanilla Raspbian install, as of
2017-06-17. Also `sudo apt install mosquitto`, if you want to run the broker
locally.
"""
import time
import paho.mqtt.client as mqtt
from instruments import instruments, ALL

mqttc = mqtt.Client()
# Edit the following line with the IP address of your MQTT broker.
mqtt_server = "10.0.1.3"
# mqtt_server = "192.168.0.8"
# mqtt_server = "127.0.0.1"


def message(topic, payload):
    """Abstract out MQTT connection.

    Since it has to be done for each message, wrap it in a function.
    """
    mqttc.connect(mqtt_server, 1883)
    mqttc.publish("orchestra/" + topic, payload)
    # time.sleep(0.2)


def twitch(robots):
    """Send all active robots a twitch command."""
    set_active(robots)
    message("twitch", 1)


def set_active(robots):
    """Activate a set of robots."""
    for robot in robots:
        message(instruments[robot], 1)
        time.sleep(0.02)


def set_inactive(robots):
    """Deactivate a set of robots."""
    for robot in robots:
        message(instruments[robot], 0)
        time.sleep(0.02)


def send_beats(robots, beat_pattern):
    """Send a beat pattern to a robot."""
    set_active(robots)
    message("beats", beat_pattern)
    time.sleep(0.02)
    set_inactive(robots)


def play(robots):
    """Activate all robots, then issue the play command."""
    set_active(robots)
    message("play", 1)
    set_inactive(robots)


def playset(beatset):
    """Sends the current beat to all 8 channels at once."""
    message("playset", beatset)
