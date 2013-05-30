# FlashLED.py
# This program toggles an LED placed
# on the GPIO pins
#
# We seem to have a Raspberry PI version 1.
# pin 6 is ground
# pin 7 is GPIO 4 which gets toggled.
#
# RPi.GPIO access /dev/mem which requires sudo
# example: sudo python FlashLED.py

import time
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

while True:
	GPIO.output(7,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(7,GPIO.LOW)
	time.sleep(1)
