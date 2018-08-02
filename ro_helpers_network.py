"""Shared networking code.

Loads and configures MQTT. Minimal functionality, but shared
across multiple scripts.

Scripts including this module will need to raise their own
on_connect and on_message functions.
"""

import paho.mqtt.client as mqtt

# Configuration for MQTT broker
mqttc = mqtt.Client()
mqtt_server = "10.0.1.3"
#mqtt_server = "127.0.0.7"

def message(topic, payload):
    """Send MQTT messages."""
    mqttc.connect(mqtt_server, 1883)
    mqttc.publish(topic, payload)

