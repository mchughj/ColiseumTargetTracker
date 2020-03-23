
import random

def initSensor() -> None:
    pass

def sensorDetect() -> bool:
    r = random.random()
    if r < 0.000001:
        return True
    else:
        return False

