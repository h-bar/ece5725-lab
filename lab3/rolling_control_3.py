# wsn8, yz2626, Rolling control, 3/4/2020
import pygame
from pygame.locals import *   # for event MOUSE variables
import os
import RPi.GPIO as GPIO
import subprocess
import time

#Broadcom numbering
GPIO.setmode(GPIO.BCM)

#os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
#os.putenv('SDL_FBDEV', '/dev/fb1')     
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
#pygame.mouse.set_visible(False)

# Button positions
quitx = 200
quity = 220
stopx = 140
stopy = 150

# Circle Position
circlex = stopx
circley = stopy
radius = 20

WHITE = 255, 255, 255
BLACK = 0,0,0
screen = pygame.display.set_mode((320, 240))
my_font= pygame.font.Font(None, 50)
my_buttons= { 'QUIT':(quitx,quity), 'STOP':(stopx,stopy)}
#my_buttons = {'Quit':(140,200)}


Lmotor_font = pygame.font.Font(None, 30)
pos_pos = (160, 100)


screen.fill(BLACK)               # Erase the Work space     

for my_text, text_pos in my_buttons.items():    
    text_surface = my_font.render(my_text, True, WHITE)
    rect = text_surface.get_rect(center=text_pos)
    #draw a circle
    pygame.draw.circle(screen,(1,0,0), (circlex, circley),radius, 0)
    screen.blit(text_surface, rect)
    pygame.display.flip()

#Detect input
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

run = True

# Timeout protocol
startTime = time.time()
while run:
   # if (time.time()-startTime) >= 10: # Time out at 10 seconds
       # print "The program has timed-out"
       # run = False
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            if y > (circley-radius) and y < (circley+radius):  # within y
                if x > (circlex-radius) and x< (circlex+radius): # stop button x range
                    print "Stop Button Pressed"
		    run = False

                    #kill the motors
                #else:
                 #   print ("Touch at ",x , y)
		 #   screen.fill(BLACK)               # Erase the Work space

		 #   for my_text, text_pos in my_buttons.items():
                 #       text_surface = my_font.render(my_text, True, WHITE)
                 #       #draw a circle
                 #       stopcircle = pygame.draw.circle(text_surface,(1,0,0), (circlex, circley),100, 0)
                 #       rect = text_surface.get_rect(center=text_pos)
                 #       screen.blit(text_surface, rect)


GPIO.cleanup()


