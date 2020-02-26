import pygame     # Import pygame graphics library
import os    # for OS calls
import time

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

pygame.init()

size = width, height = 320, 240 
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball = pygame.image.load("magic_ball.png")


balls = [pygame.transform.scale(ball, (60, 60)), pygame.transform.scale(ball, (40, 40))] 
speeds = [[2,2], [4, 4]]
ballrects = []
for a_ball in balls:
  ballrects.append(a_ball.get_rect())

while 1:
	time.sleep(0.02)
	screen.fill(black) 

	for i in range(len(balls)):
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
		
	pygame.display.flip()   
