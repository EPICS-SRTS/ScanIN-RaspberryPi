import RPi.GPIO as GPIO 

import time 
import time
import serial
import binascii

 

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False) 

# Pin Numbers
red_led = 18
green_led = 24
blue_led = 25

# Set pins to output mode
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(blue_led, GPIO.OUT)

while True:
    #RED LED
    GPIO.output(red_led,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(red_led,0)
    #GREEN LED
    GPIO.output(green_led,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(green_led,0)
    #BLUE LED
    GPIO.output(blue_led,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(blue_led,0)

GPIO.cleanup()

