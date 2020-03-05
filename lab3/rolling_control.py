# Quit Button Setup
from signal import signal, SIGINT
from sys import exit

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

quit_button = 17
GPIO.setup(quit_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def _quit():
    GPIO.cleanup()
    exit(0)

def quit_cb(channel):
    _quit()

def quit_sig(signal_received, frame):
    _quit()

# GPIO.add_event_detect(quit_button, GPIO.FALLING, callback=quit_cb, bouncetime=300)
signal(SIGINT, quit_sig)


# Actual code starts from here
import time
import sys

interval = 0.02

motor_stop = 0.0015
motor_r_max = 0.0017
motor_f_max = 0.0013


def initMotor(pwm_pin):
    GPIO.setup(pwm_pin, GPIO.OUT)
    motor = GPIO.PWM(pwm_pin, 60)
    startMotor(motor)
    setPMotor(motor, motor_stop)

    return motor

def setMotor(pwm, high, low):
    f = 1 / (high + low)
    pw = high
    dc = high / (high + low) * 100
    print "Setting Motor -> F: {}\tPW: {}\tDC: {}".format(f, pw, dc)  
    
    pwm.ChangeFrequency(f)
    pwm.ChangeDutyCycle(dc)

def setPMotor(pwm, high):
    setMotor(pwm, high, interval)

def startMotor(pwm):
    pwm.ChangeFrequency(1 / interval)
    pwm.start(motor_stop / (motor_stop + interval) * 100)

def cmdMotor(pwm, cmd):
    if cmd == 'f':
        setPMotor(pwm, motor_f_max)
    elif cmd == 'r':
        setPMotor(pwm, motor_r_max)
    elif cmd == 'i':
        setPMotor(pwm, motor_stop)


if len(sys.argv) > 1:
    frequency = int(sys.argv[1])


l_motor = initMotor(5)
r_motor = initMotor(6)

def button_cb(channel):
    if channel == 17:
        cmdMotor(l_motor, 'f')
    elif channel == 22:
        cmdMotor(l_motor, 'i')
    elif channel == 23:
        cmdMotor(l_motor, 'r')
    elif channel == 27:
        cmdMotor(r_motor, 'f')
    elif channel == 19:
        cmdMotor(r_motor, 'i')
    elif channel == 26:
        cmdMotor(r_motor, 'r')

for pin in [17, 22, 23, 27, 19, 26]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_cb, bouncetime=300)


import pygame
from pygame.locals import *

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT#   
os.putenv('SDL_FBDEV', '/dev/fb1')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0

screen = pygame.display.set_mode((320, 240))

banner_font = pygame.font.Font(None, 30)
banners = [
    {
        'text': 'Left History',
        'pos': (20, 20)
    }
    {
        'text': 'Right History',
        'pos': (40, 40)
    }
]

while True:
    screen.fill(black)
    for b in banners:    
        text_surface = banner_font.render(b.text, True, WHITE)    
        rect = text_surface.get_rect(left=text_pos)
        screen.blit(text_surface, rect)
    pygame.display.flip()
# raw_input()

l_motor.stop()
r_motor.stop()
_quit()
