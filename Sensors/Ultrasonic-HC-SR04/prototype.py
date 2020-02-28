#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

def cmToNearestObject():
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()

  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  # At sea level the speed of sound is 343 meters per second.  
  # We divide by two because of the return trip time of the 
  # ultrasonic sound wave.  Also we are using centimeters here
  # as our metric.
  distance = (elapsed * 34300)/2

  return distance


# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO    = 24

print("Prototype usage of an ultrasonic sensor - the HC-sR04")

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
