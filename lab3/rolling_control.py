# William Nunez, Yan Zhang, wsn8, yz2626, wed, 3/4/2020
import pygame     # Import pygame graphics library
import os    # for OS calls
import time
from pygame.locals import *   # for event MOUSE variables

import RPi.GPIO as GPIO
import time
import subprocess # For interrupt
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
    print "Falling edge detected on button 17"
    GPIO.cleanup()
    exit(0)
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)


os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT#   
os.putenv('SDL_FBDEV', '/dev/fb1')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0
screen = pygame.display.set_mode((320, 240))
l1_font= pygame.font.Font(None, 50)
l1_buttons= { 
    'STOP':(170,120),  # Position of stop button
    'QUIT':(240,180)   # position of quit button
}

#l2_font = pygame.font.Font(None, 25)
#l2_buttons = {
#    'pause': (40, 200),
#    'Fast': (120,200),
#    'Slow': (200, 200),
#    'Back': (280, 200)
#}

pos_font = pygame.font.Font(None, 30)
pos_pos = (160, 100)

size = width, height = 320, 240 
black = 0, 0, 0
screen = pygame.display.set_mode(size)
#ball = pygame.image.load("magic_ball.png")


#balls = [pygame.transform.scale(ball, (60, 60)), pygame.transform.scale(ball, (4
#speeds = [[2,2], [4, 4]]
#ballrects = []

#for a_ball in balls:
#  ballrects.append(a_ball.get_rect())

for my_text, text_pos in l1_buttons.items():    
    text_surface = l1_font.render(my_text, True, WHITE)    
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)
    pygame.display.flip()


playback = False
pause = False
level1 = True
step = 5
while True:
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):           
            pos = pygame.mouse.get_pos() 
            x,y = pos
            if level1:
                if y > 120:                
                    if x < 160:
                        print "start button pressed"
                        playback = True
                        level1 = False
                    else:
                        print "quit button pressed"
                        exit(0)
            else:
                if y > 160:
                    if x < 80:
                        print "pause button pressed"
                        pause = not pause
                    elif x < 160:
                        print "fast button pressed"
                        speeds[0][0] += step
                        speeds[0][1] += step
                        speeds[1][0] += step
                        speeds[1][0] += step
                    elif x < 240: 
                        print "slow button pressed"
                        speeds[0][0] -= step
                        speeds[0][1] -= step
                        speeds[1][0] -= step
                        speeds[1][0] -= step
                    else:
                        print "back button pressed"
                        playback = False
                        level1= True
            
            screen.fill(black)
            
            if level1:
                for my_text, text_pos in l1_buttons.items():    
                    text_surface = l1_font.render(my_text, True, WHITE)    
                    rect = text_surface.get_rect(center=text_pos)
                    screen.blit(text_surface, rect)
            
                text_surface = pos_font.render("touch at " + str(pos), True, WHITE)    
                rect = text_surface.get_rect(center=pos_pos)
            
                screen.blit(text_surface, rect)
            else:
                for my_text, text_pos in l2_buttons.items(): 
                    text_surface = l2_font.render(my_text, True, WHITE)    
                    rect = text_surface.get_rect(center=text_pos)
                    screen.blit(text_surface, rect)
    
            pygame.display.flip()


    if playback == True:
	time.sleep(0.02)
       
        screen.fill(black) 
	for i in range(len(balls)):
	    if pause == False:
                ballrects[i] = ballrects[i].move(speeds[i])
    
                if ballrects[i].left < 0 or ballrects[i].right > width:
                    speeds[i][0] = -speeds[i][0]
	        if ballrects[i].top < 0 or ballrects[i].bottom > height:
		    speeds[i][1] = -speeds[i][1]

                for j in range(len(balls)):
	            if i == j:
		        continue
		    if not ballrects[i].colliderect(ballrects[j]):
		        continue
		
                    if ballrects[i].left < ballrects[j].left and ballrects[i].right >= ballrects[j].left and speeds[i][0] > 0:
		        speeds[i][0] = -speeds[i][0]
		    if ballrects[i].right > ballrects[j].right and ballrects[i].left <= ballrects[j].right and speeds[i][0] < 0:
		        speeds[i][0] = -speeds[i][0]

                    if ballrects[i].top < ballrects[j].top and ballrects[i].bottom >= ballrects[j].top and speeds[i][1] > 0:
		        speeds[i][1] = -speeds[i][1]
		    if ballrects[i].bottom > ballrects[j].bottom and ballrects[i].top <= ballrects[j].bottom and speeds[i][1] < 0:
		        speeds[i][1] = -speeds[i][1]
	
            screen.blit(balls[i], ballrects[i])   # Combine Ball surface with workspace surface
	
        for my_text, text_pos in l2_buttons.items():    
            text_surface = l2_font.render(my_text, True, WHITE)    
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
       	  	
	pygame.display.flip()   
