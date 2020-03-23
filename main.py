#!/usr/bin/env python3

import sys
import os

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
    return parser


def main(args):
    white = (255, 255, 255) 
    green = (0, 255, 0) 
    blue = (0, 0, 128) 
    black = (0, 0, 0) 

    pygame.init()
    
    if args.windowed:
        width = 800
        height = 600
        display_surface = pygame.display.set_mode((width,height), pygame.RESIZABLE, 16)
    else:
        width = 1024
        height = 768
        display_surface = pygame.display.set_mode((width,height), pygame.FULLSCREEN, 16)

    font = pygame.font.SysFont('bitstreamverasansmono', args.fontSize) 
     
    text = font.render('1', True, black, white) 

    if not args.horizontal:
        text = pygame.transform.rotate(text, 90)
      
    # create a rectangular object for the 
    # text surface object 
    textRect = text.get_rect()  
      
    # set the center of the rectangular object. 
    textRect.center = (width // 2, height // 2) 
      
    while True: 
        # completely fill the surface object 
        # with white color 
        display_surface.fill(white) 
      
        # copying the text surface object 
        # to the display surface object  
        # at the center coordinate. 
        display_surface.blit(text, textRect) 
      
        # iterate over the list of Event objects 
        # that was returned by pygame.event.get() method. 
        for event in pygame.event.get() : 
      
            # if event object type is QUIT 
            # then quitting the pygame 
            # and program both. 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                quit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit() 
                    quit() 
      
            # Draws the surface object to the screen.   
            pygame.display.update()  


if __name__ == "__main__":
    parser = initArgs()
    args = parser.parse_args()
    main(args)
