import pygame     # Import pygame graphics library
import os    # for OS calls

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0')   

pygame.init()

size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball = pygame.image.load("magic_ball.png")
ball2 = pygame.transform.scale(pygame.image.load("magic_ball.png"), (10, 10))

speed = [1,1]
ballrect = ball.get_rect()

speed2 = [2,2]
ballrect2 = ball2.get_rect()

while 1:
    ballrect = ballrect.move(speed)
    ballrect2 = ballrect2.move(speed2)
    
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
    
    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]
    if ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]
    
    if not ballrect.colliderect(ballrect2):
        if ballrect.left < ballrect2.right or ballrect.right > ballrect2.left: 
            speed[0] = -speed[0]
            speed2[0] = -speed2[0]    
        if ballrect.top < ballrect2.bottom or ballrect.bottom > ballrect2.top:
            speed[1] = -speed[1]
            speed2[1] = -speed2[1]



    screen.fill(black)      # Erase the Work space     
                     
    screen.blit(ball, ballrect)   # Combine Ball surface with workspace surface
    screen.blit(ball, ballrect2)
    pygame.display.flip()  # display workspace on screen
