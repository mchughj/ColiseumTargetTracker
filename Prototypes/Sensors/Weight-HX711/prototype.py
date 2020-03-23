#!/usr/bin/python3

import time
import sys

referenceUnit = -10

import RPi.GPIO as GPIO
from hx711 import HX711

hx = HX711(17, 27)
hx.power_up()

# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(referenceUnit)

hx.reset()
print("Beginning tare")
hx.tare(100)
print("Tare done! Offset computed: {}.".format(hx.get_offset()))

try:
    while True:
        val_average = hx.get_average_weight(6)
        val_median = hx.get_weight(6)
        print("Weight: {} avg, {} median".format(val_average, val_median))

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

except (KeyboardInterrupt, SystemExit):
    print("Exiting...")
    GPIO.cleanup()
