#!/usr/bin/env python3

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

def initArgs() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser( 
            usage = "%(prog)s OPTIONs",
            description = "Run the Coliseum target tracker application"
    )
    parser.add_argument(
            "-v", "--version", action="version",
            version = f"{parser.prog} version 1.0.0"
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
    showCenteredText("Read?", displaySurface, smallerFont, width, height)
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
    gameRunning = False

    initSensor()
    initController()

    showCenteredText("Ready?", displaySurface, smallerFont, width, height)

    while True: 
        currentMillis = int(round(time.time() * 1000)) 
      
        if nextRedraw < currentMillis and gameRunning:
            updateScreen(displaySurface, font, score, width, height)
            nextRedraw = currentMillis + int(1000 / REFRESH_RATE_HZ)

        if sensorDetect():
            score += 1

        if controllerIncreaseScore():
            score += 1

        if controllerDecreaseScore():
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
