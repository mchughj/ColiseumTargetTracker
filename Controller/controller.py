import time
import RPi.GPIO as GPIO
   
# BCM Pins used by the installation for the various buttons
# Although the Raspberry PI documentation suggests that all pins have pull up resisters 
# that can be set via software my experience suggests otherwise.  Using this:
#
#    python3 -c '
#       import RPi.GPIO as GPIO
#       GPIO.setmode(GPIO.BCM)
#       pin = 22
#       GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#       print(GPIO.input(pin))
#    '
# For high number pins it prints "0" when of course it shouldn't if nothing is attached.
# 
# Pins defined below work well.
#
#                         UPPER RIGHT
#  +---------+---------+ x
#  |  3V     |   5V    |
#  |  GPIO2  |   5V    |
#  |  GPIO3  |   GND   |
#  |  GPIO4  | GPIO14  |
#  |  GND    | GPIO15  |

GPIO_SCORE_UP     = 14
GPIO_SCORE_DOWN   = 4
GPIO_START_GAME   = 3
GPIO_STOP_MACHINE = 15

buttons = [GPIO_SCORE_UP, GPIO_SCORE_DOWN, GPIO_START_GAME, GPIO_STOP_MACHINE]

buttonState = {}

def initController() -> None:
    print ("InitController;")
    GPIO.setmode(GPIO.BCM)

    # Setup all the button pins
    for b in buttons:
        GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        buttonState[b] = False
        GPIO.add_event_detect(b, GPIO.FALLING, callback=setButtonPressed, bouncetime=400)

def setButtonPressed(pin):
    buttonState[pin] = True

def getButtonState(pin) -> bool:
    result = buttonState[pin]
    buttonState[pin] = False
    return result

def controllerIncreaseScore() -> bool:
    result = getButtonState(GPIO_SCORE_UP)
    if result:
        print( "controllerIncreaseScore - button is down")
    return result

def controllerDecreaseScore() -> bool:
    result = getButtonState(GPIO_SCORE_DOWN)
    if result:
        print( "controllerDecreaseScore - button is down")
    return result

def controllerStartGame() -> bool:
    result = getButtonState(GPIO_START_GAME)
    if result:
        print( "controllerStartGame - button is down")
    return result
