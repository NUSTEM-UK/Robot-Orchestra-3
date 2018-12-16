// Playback-responsive twinkly lights, for extra festivityness.
// This version sets each pixel to one of red, green, or white.

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

#define PIN D1
#define NUMPIXELS 60
#define BRIGHTNESS 255

// Network & MQTT configuration

const char* ssid = "nustem";
const char* password = "nustem123";

// Stick the IP address of the MQTT server in the line below.
const char* mqtt_server = "10.0.1.3";

// NeoPixel string configuration
// See NeoPixel strandtest for details. First argument is number of pixels
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

// Globals

// For historic reasons, we call these Wemos boards 'skutters'.
String subString;
char skutterNameArray[60];
int myChannel;
int myOldChannel;
int units;
int twos;
int fours;

// Each robot has a unique name, generated from the hardware MAC address.
// These variables will store those names.
String huzzahMACAddress;
String skutterNameString;
String subsTargetString;
char subsTargetArray[60];

// Variables for the wifi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);


void setup() {
    strip.begin();
    strip.show(); // Initialize all pixels to 'off'
    
    Serial.begin(115200);
    setup_wifi();
    
    // Set up on-board LEDs for diagnostics
    pinMode(BUILTIN_LED, OUTPUT);
    pinMode(02, OUTPUT);
        
    // Get this Huzzah's MAC address and use it to register with the MQTT server
    huzzahMACAddress = WiFi.macAddress();
    skutterNameString = "skutter_" + huzzahMACAddress;
    Serial.println(skutterNameString);
    skutterNameString.toCharArray(skutterNameArray, 60);
    subsTargetString = "orchestra/" + skutterNameString;
    subsTargetString.toCharArray(subsTargetArray, 60);
    for (int i = 0; i < 60; i++) {
        Serial.print(subsTargetArray[i]);
    }
    Serial.println();
    
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);

}

void loop() {
    // Call the MQTT client to poll for updates, reconnecting if necessary
    // Handle messages via the callback function
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}


void callback(char* topic, byte* payload, unsigned int length) {

    // Convert topic and message to C++ String types, for ease of handling

    // message length gives us the length of the payload
    String payloadString;
    for (int i = 0; i < length; i++) {
        payloadString += String((char)payload[i]);
    }

    // for the topic, we need to call strlen to find the length
    String topicString;
    for (int i = 0; i < strlen(topic); i++) {
        topicString += String((char)topic[i]);
    }

    // Debug: print the (processed) received message to serial
    Serial.print(F("Message arrived ["));
    Serial.print(topicString);
    Serial.print(F("] "));
    Serial.println(payloadString);

    // Now handle the possible messages, matching on topic
    // For this use, we've stripped everything out that's not necessary.

    /* HANDLE RECEIVED BEAT SET - LIVE PLAYBACK *****************/
    if (topicString == "orchestra/playset") {
        Serial.println(F("UDPATE!"));

        for (int i = 0; i < NUMPIXELS; i++) {
            switch(random(0,3)) {
                case 0:
                    // Pixel going RED
                    strip.setPixelColor(i, strip.Color(random(0,BRIGHTNESS), 0, 0));
                    break;
                case 1:
                    // Pixel going GREEN
                    strip.setPixelColor(i, strip.Color(0, random(0,BRIGHTNESS), 0));
                    break;
                case 2:
                    // Pixel going WHITE
                    { // Need brackets to assign a variable here
                        int ungreyness = random(0, BRIGHTNESS);
                        strip.setPixelColor(i, strip.Color(ungreyness, ungreyness, ungreyness));
                        
                    }
                    break;
                default:
                    strip.setPixelColor(i, strip.Color(0,0,0));
            }
        }        
        strip.show();
        
        delay(50);
        // ...and turn the LED off
        digitalWrite(BUILTIN_LED, LOW);
    }
}
