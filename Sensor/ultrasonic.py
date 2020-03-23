
import time
import statistics
import RPi.GPIO as GPIO
   
# BCM Pins used by the ultrasonic sensor. 
# Note that the Raspberry PI is a 3.3 volt device
# so protect the ECHO pin using a 1K and 2K resister voltage divider.
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

STEADY_STATE_READINGS = 50
STEADY_STATE_PAUSE_SECONDS = 0.1
STEADY_STATE_TRIM_PERCENTAGE = 0.2

steadyStateCM = 0
varianceSteadyStateCM = 0

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


def initSensor() -> None:
    GPIO.setmode(GPIO.BCM)
    # Set pins as output and input
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # Initialize the trigger to low
    GPIO.output(GPIO_TRIGGER, False)

    distances = []
    for i in range(STEADY_STATE_READINGS):
        distances += [cmToNearestObject()]
        time.sleep(STEADY_STATE_PAUSE_SECONDS)

    distances.sort()
    trimAmount = int(len(distances) * STEADY_STATE_TRIM_PERCENTAGE )
    distances = distances[trimAmount:-trimAmount]
    
    steadyStateCM = statistics.mean(distances)
    varianceSteadyStateCM = statistics.variance(distances)

    print( "Init ultrasonic sensor complete; steadyStateCM: {}, varianceSteadyStateCM: {}".format(
        steadyStateCM, varianceSteadyStateCM))

def sensorDetect() -> bool:
    distance = cmToNearestObject()

    if distance < steadyStateCM - varianceSteadyStateCM:
        return True
    else:
        return False

