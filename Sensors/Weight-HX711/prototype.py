#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

GPIO_TRIGGER = 23
GPIO_ECHO    = 24


# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

print("Prototype usage of a weight sensor - the HX711")

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

# Protect the Raspberry PI by using a 1K and 2K resister voltage divider.
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:
  while True:
    distance = cmToNearestObject()
    print "Distance : %.1f cms" % distance
    time.sleep(2)

except KeyboardInterrupt:
  GPIO.cleanup()
