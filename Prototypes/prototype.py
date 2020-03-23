import pygame.display

white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
black = (0, 0, 0) 

width = 1024
height = 768

pygame.init()
display_surface = pygame.display.set_mode((width,height), pygame.FULLSCREEN, 16)

font = pygame.font.SysFont('bitstreamverasansmono', 768) 
 
text = font.render('1', True, black, white) 
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
            if event.key == pygame.K_q || event.key == pygame.K_ESC:
                pygame.quit() 
                quit() 
  
        # Draws the surface object to the screen.   
        pygame.display.update()  

