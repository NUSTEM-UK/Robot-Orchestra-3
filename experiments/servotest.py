from gpiozero import Device, Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

Device.pin_factory = PiGPIOFactory()

myservo = [Servo(27), Servo(22), Servo(5), Servo(6),
           Servo(13), Servo(19), Servo(26), Servo(21)]

for i in range(8):
    myservo[i].min()
    sleep(0.1)

sleep(1)

for i in range(8):
    myservo[i].mid()
    sleep(0.1)
    myservo[i].min()
    sleep(0.1)

