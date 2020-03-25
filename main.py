#!/usr/bin/env python3

# Main program for the Coliseum V Target Tracker

import sys
import os
import time

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Enable print
def enablePrint():
    sys.stdout = sys.__stdout__

# I don't like seeing the pygame version on stdout
blockPrint()
import pygame.display
enablePrint()

import argparse


WHITE = (255, 255, 255) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 128) 
BLACK = (0, 0, 0) 
REFRESH_RATE_HZ = 30
VERSION = 1.0

def initArgs() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser( 
            usage = "%(prog)s OPTIONs",
            description = "Run the Coliseum target tracker application"
    )
    parser.add_argument(
            "-v", "--version", action="version",
            version = "Version {}".format(VERSION)
    )
    parser.add_argument(
            "-w", "--windowed", 
            help = "Run the program in a window and not full screen.",
            default = False, action ="store_true"
    )
    parser.add_argument(
            "--horizontal", 
            help = "Run the program in horizontal and not vertical mode.", 
            default = False, action ="store_true"
    )
    parser.add_argument(
            "--fontSize", 
            help = "Set the font size value.  Useful when running windowed.", 
            default = 768, type=int
    )
    parser.add_argument(
            "--fakeSensor", 
            help = "Use a fake sensor that randomly generates hits",
            default = False, action = "store_true"
    )
    parser.add_argument(
            "--sensorThreshold", 
            help = "The percentage difference between steady state and a new sensor value that will trigger a positive hit.  A larger value will result in more false positives.  Default is 0.2", 
            default = 0.2, type=float
    )
    parser.add_argument(
            "--sensorTriggerCooldownMillis", 
            help = "The number of milliseconds that must pass before another positive sensor value will be considered valid.  This stops a single shot into goal from bouncing around and being registered multiple times while still allowing for multiple distinct shots to be counted.  Too low of a value increases the false positives and too high of a value increases false negatives.  Default is 3000 milliseconds.", 
            default = 3000, type=float
    )
    parser.add_argument(
            "--sensorHz", 
            help = "The number of sensor values taken per second.  Various environmental factors will play into choosing a good value here.  For example, using an ultrasonic sensor and too high of a value will cause the sensor to pick up echos of reflections from prior readings.  Too low of a number and you may increase your false negatives.  Default is 30 hertz which is about 33 millisecond delay between readings.",
            default = 30, type=float
    )
    return parser

def showCenteredText(textString, displaySurface, font, width, height) -> None:
    text = font.render(textString, True, BLACK, WHITE) 

    if not args.horizontal:
        text = pygame.transform.rotate(text, 90)
      
    # create a rectangular object for the 
    # text surface object 
    textRect = text.get_rect()  
      
    # set the center of the rectangular object. 
    textRect.center = (width // 2, height // 2) 
      
    # Background color 
    displaySurface.fill(WHITE) 

    # copying the text surface object 
    # to the display surface object  
    # at the center coordinate. 
    displaySurface.blit(text, textRect) 
    pygame.display.update()  

def updateScreen(displaySurface, font, score, width, height) -> None:
    showCenteredText(str(score), displaySurface, font, width, height)

def showGameStart(displaySurface, smallerFont, font, score, width, height) -> None:
    showCenteredText("Ready?", displaySurface, smallerFont, width, height)
    time.sleep(1)
    showCenteredText("3", displaySurface, font, width, height)
    time.sleep(1)
    showCenteredText("2", displaySurface, font, width, height)
    time.sleep(1)
    showCenteredText("1", displaySurface, font, width, height)
    time.sleep(1)
    showCenteredText("GO!", displaySurface, smallerFont, width, height)
    time.sleep(0.5)


def main(args) -> None:

    if args.fakeSensor:
        from Sensor.fakesensor import initSensor, sensorDetect
    else:
        from Sensor.ultrasonic import initSensor, sensorDetect

    from Controller.controller import initController, controllerIncreaseScore, controllerDecreaseScore, controllerStartGame

    pygame.init()
    
    if args.windowed:
        width = 800
        height = 600
        displaySurface = pygame.display.set_mode((width,height), pygame.RESIZABLE, 16)
    else:
        width = 1024
        height = 768
        displaySurface = pygame.display.set_mode((width,height), pygame.FULLSCREEN, 16)

    smallerFont = pygame.font.SysFont('bitstreamverasansmono', int(args.fontSize/2))
    font = pygame.font.SysFont('bitstreamverasansmono', args.fontSize) 
    score = 0
    nextRedraw = 0
    nextSensorDetect = 0
    nextAllowableSensorTrigger = 0
    gameRunning = False

    initSensor(args.sensorThreshold)
    initController()

    showCenteredText("Ready?", displaySurface, smallerFont, width, height)

    while True: 
        t = time.time()
        currentMillis = int(round(t * 1000)) 
      
        if nextRedraw < currentMillis and gameRunning:
            updateScreen(displaySurface, font, score, width, height)
            nextRedraw = currentMillis + int(1000 / REFRESH_RATE_HZ)

        if nextSensorDetect < currentMillis and gameRunning:
            if sensorDetect():
                if nextAllowableSensorTrigger < currentMillis:
                    score += 1
                    nextAllowableSensorTrigger = currentMillis + args.sensorTriggerCooldownMillis
                else:
                    print("ignoring the subsequent reading;")
            nextSensorDetect = currentMillis + int(1000 / args.sensorHz)

        if controllerIncreaseScore():
            score += 1

        if controllerDecreaseScore():
            if score > 0:
                score -= 1

        if controllerStartGame():
            gameRunning = True
            showGameStart(displaySurface, smallerFont, font, score, width, height)
            score = 0
      
        # Iterate over the list of pygame event objects 
        for event in pygame.event.get(): 
            # Look for conditions under which we should stop the 
            # execution of the program.
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_q or event.key == pygame.K_ESCAPE
                )
            ):
                pygame.quit() 
                quit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    score += 1
                elif event.key == pygame.K_d:
                    score -= 1


if __name__ == "__main__":
    parser = initArgs()
    args = parser.parse_args()
    main(args)
