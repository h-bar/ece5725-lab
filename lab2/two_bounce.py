import pygame # Import pygame graphics library
import os # for OS calls


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



os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()

size = width, height = 320, 240
speed = [2,2]
black = 0, 0, 0

speed2 = [1,1]

screen = pygame.display.set_mode(size)
ball = pygame.image.load("magic_ball.png")
ballrect = ball.get_rect()

ball2 = pygame.image.load("magic_ball.png")
ballrect2 = ball2.get_rect()

while 1:
	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]

	ballrect2 = ballrect2.move(speed2)
        if ballrect2.left < 0 or ballrect2.right > width:
                speed2[0] = -speed2[0]
        if ballrect2.top < 0 or ballrect2.bottom > height:
                speed2[1] = -speed2[1]

	screen.fill(black) # Erase the Work space
	screen.blit(ball, ballrect) # Combine Ball surface with workspace surface
	screen.blit(ball2, ballrect2)
	pygame.display.flip() # display workspace on screen
