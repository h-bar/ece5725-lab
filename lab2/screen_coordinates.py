# wsn8, yz2626, this program works
import pygame
from pygame.locals import *   # for event MOUSE variables
import os
import RPi.GPIO as GPIO
import subprocess
import time

#Broadcom numbering
GPIO.setmode(GPIO.BCM)

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


# take button input
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Define quit callback
def GPIO17_callback(channel):
                print "Bail-out Button Pressed"
		#run  = False
		exit()

pygame.init()
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0
screen = pygame.display.set_mode((320, 240))
my_font= pygame.font.Font(None, 50)
#my_buttons= { 'Start':(80,180), 'Quit':(240,180)}
my_buttons = {'Quit':(140,200)}

pos_font = pygame.font.Font(None, 30)
pos_pos = (160, 100)


screen.fill(BLACK)               # Erase the Work space     

for my_text, text_pos in my_buttons.items():    
    text_surface = my_font.render(my_text, True, WHITE)    
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)
    pygame.display.flip()

#Detect input
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

run = True

# Timeout protocol
startTime = time.time()
while run:
    if (time.time()-startTime) >= 10: # Time out at 10 seconds
        print "The program has timed-out"
        run = False
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            if y > 160:  # Lower than a certain y
                if x > 130 and x<170: # Quit button x range
                    print "Quit Button Pressed"
		    run = False
                else:
                    print ("Touch at ",x , y)
		    screen.fill(BLACK)               # Erase the Work space

		    for my_text, text_pos in my_buttons.items():
                        text_surface = my_font.render(my_text, True, WHITE)
                        rect = text_surface.get_rect(center=text_pos)
                        screen.blit(text_surface, rect)

                        text_surface = pos_font.render("Touch at " + str(pos), True, WHITE)
                        rect = text_surface.get_rect(center=pos_pos)

                    screen.blit(text_surface, rect)
                    pygame.display.flip()
	    else:
	         print ("Touch at ",x , y)
                 screen.fill(BLACK)               # Erase the Work space

                 for my_text, text_pos in my_buttons.items():
                     text_surface = my_font.render(my_text, True, WHITE)
                     rect = text_surface.get_rect(center=text_pos)
                     screen.blit(text_surface, rect)

                     text_surface = pos_font.render("Touch at " + str(pos), True, WHITE)
                     rect = text_surface.get_rect(center=pos_pos)

                 screen.blit(text_surface, rect)
                 pygame.display.flip()


