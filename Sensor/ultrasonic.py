
# This python module works with the Ultrasonic HC-SR04 hardware
# component.  

import time
import statistics
import RPi.GPIO as GPIO
   
# BCM Pins used by the ultrasonic sensor. 
# Note that the Raspberry PI is a 3.3 volt device
# so protect the ECHO pin using a 1K and 2K resister voltage divider.
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

STEADY_STATE_READINGS = 35
STEADY_STATE_PAUSE_SECONDS = 0.1
STEADY_STATE_TRIM_PERCENTAGE = 0.2

steadyStateCM = 0
varianceCM = 0
sensorThreshold = 0.2
lowValueThreshold = 0

def cmToNearestObject():
    # Toggle the trigger pin so that it knows to begin a 
    # distance check.
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Echo pin will go from low to high and then remain high
    # until the sound is reflected back to the sensor.  Then
    # it will move back to low.
    # 
    # The total time spent high is the amount of time it took
    # for the sound to be reflected back and the travel distance
    # is one half of the time.
    start = time.time()
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    stop = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    elapsed = stop-start

    # At sea level the speed of sound is 343 meters per second.  
    # We divide by two because of the return trip time of the 
    # ultrasonic sound wave.  343 meters is 34300 centimeters 
    # which is a better unit of measure for this application.
    distance = (elapsed * 34300)/2
  
    return distance


def initSensor(percentageSensorThreshold) -> None:
    global steadyStateCM, varianceCM, sensorThreshold, lowValueThreshold

    sensorThreshold = percentageSensorThreshold

    print("initSensor - starting up; sensorThreshold: {}, trigger: {}, echo: {}".format(
        sensorThreshold, GPIO_TRIGGER, GPIO_ECHO))

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # Initialize the trigger to low.  The 
    GPIO.output(GPIO_TRIGGER, False)

    print("initSensor - starting gathering data; numberSamples: {}".format(STEADY_STATE_READINGS))
    distances = []
    for i in range(STEADY_STATE_READINGS):
        v = cmToNearestObject()
        print("initSensor; sample: {}, value: {}".format(i, v))
        distances += [v]
        time.sleep(STEADY_STATE_PAUSE_SECONDS)

    distances.sort()
    trimAmount = int(len(distances) * STEADY_STATE_TRIM_PERCENTAGE )

    lowValues = ', '.join(map("{:0.2f}".format,distances[0:trimAmount]))
    highValues = ', '.join(map("{:0.2f}".format,distances[-trimAmount:-1]))

    print("initSensor - trimming; trimAmount: {}".format(trimAmount))
    print("initSensor - trimming; lowValues: {}".format(lowValues))
    print("initSensor - trimming; highValues: {}".format(highValues))
    distances = distances[trimAmount:-trimAmount]

    print("initSensor - trimming; remaining values: {}".format( ", ".join(map("{:0.2f}".format,distances))))
    
    steadyStateCM = statistics.mean(distances)
    varianceCM = statistics.variance(distances)
    lowValueThreshold = (steadyStateCM - varianceCM) * (1-sensorThreshold)

    print("initSensor - complete; steadyStateCM: {:0.2f}".format(steadyStateCM))
    print("initSensor - complete; varianceCM: {:0.2f}".format(varianceCM))
    print("initSensor - complete; lowValueThreshold: {:0.2f}".format(lowValueThreshold))

def sensorDetect() -> bool:
    global lowValueThreshold

    d = cmToNearestObject()

    if d < lowValueThreshold:
        print( "sensorDetect - true; d: {:0.2f}, lowValueThreshold: {:0.2f}".format(d, lowValueThreshold))
        return True
    else:
        print( "sensorDetect - false; d: {:0.2f}, lowValueThreshold: {:0.2f}".format(d, lowValueThreshold))
        return False

