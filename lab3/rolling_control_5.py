# Will Nunez, Yan Zhang, wsn8, yz2626, wed, 3/3/2020
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
import pygame
from pygame.locals import *
import os

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT#   
os.putenv('SDL_FBDEV', '/dev/fb1')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

interval = 0.02

#motor_stop = 0.0015
motor_stop = 0
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

WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0, 255, 0

pygame.init()
# pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((320, 240))

labels = [
        {
        'text': 'Quit',
        'pos': (260, 210),
        'font': pygame.font.Font(None, 30)
    },
    {
        'text': 'Left History',
        'pos': (70, 30),
        'font': pygame.font.Font(None, 30)
    },
    {
        'text': 'Right History',
        'pos': (240, 30),
        'font': pygame.font.Font(None, 30)
    },
    {
        'text': 'STOP',
        'pos': (160, 130),
        'font': pygame.font.Font(None, 40)
    }
]

stopCircle = {
    'color': RED,
    'pos': (160, 130),
    'r': 40
}

resumeCircle = {
        'color': GREEN,
        'pos': (160,130),
        'r': 40
}


l_history = ['', '', '']
r_history = ['', '', '']

l_motor = initMotor(5)
r_motor = initMotor(6)

start_time = 0

def button_cb(channel):
    log_time = time.time() - start_time
    if channel == 17:
        log_event(l_history, 'Clk', log_time)
        cmdMotor(l_motor, 'f')
    elif channel == 22:
        log_event(l_history, 'Stop', log_time)
        cmdMotor(l_motor, 'i')
    elif channel == 23:
        log_event(l_history, 'Counter-Clk', log_time)
        cmdMotor(l_motor, 'r')
    elif channel == 27:
        log_event(r_history, 'Clk', log_time)
        cmdMotor(r_motor, 'f')
    elif channel == 19:
        log_event(r_history, 'Stop', log_time)
        cmdMotor(r_motor, 'i')
    elif channel == 26:
        log_event(r_history, 'Counter-Clk', log_time)
        cmdMotor(r_motor, 'r')
    update_screen()

def gen_history_label(side, history):
    pos_x = 60 if side == 'l' else 260
    pos_y = 100
    step_y = 30
    font = pygame.font.Font(None, 20)

    return [
            {
            'text': history[0],
            'pos': (pos_x, pos_y),
            'font': font
        },
        {
            'text': history[1],
            'pos': (pos_x, pos_y + step_y),
            'font': font
        },
        {
            'text': history[2],
            'pos': (pos_x, pos_y + step_y * 2),
            'font': font
        }
    ]


def render_lables(screen, labels):
    for label in labels:
        label_surface = label['font'].render(label['text'], True, WHITE)    
        rect = label_surface.get_rect(center=label['pos'])
        screen.blit(label_surface, rect)

def update_screen():
    screen.fill(BLACK)
    if resume:
        pygame.draw.circle(screen, stopCircle['color'], stopCircle['pos'], stopCircle['r'])
    else:
        pygame.draw.circle(screen, resumeCircle['color'], resumeCircle['pos'], resumeCircle['r'])
    render_lables(screen, labels)
    render_lables(screen, gen_history_label('l', l_history))
    render_lables(screen,  gen_history_label('r', r_history))
    
    pygame.display.flip()

def log_event(history, event, log_time):
    history.pop();
    history.insert(0, '{}  {}'.format(event, int(log_time)))


resume = True # Flag for noting position of resume
def event_loop():
    while True:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):           
                pos = pygame.mouse.get_pos() 

                if pos[0] > stopCircle['pos'][0] - stopCircle['r'] and pos[0] < stopCircle['pos'][0] + stopCircle['r']:
                    if pos[1] > stopCircle['pos'][1] - stopCircle['r'] and pos[1] < stopCircle['pos'][1] + stopCircle['r']:
                        if resume:
                            #wait until resume button hit
                            update_screen()

                        else: # Stop motors and wait   
                            button_cb(22)
                            button_cb(19)
                            update_screen()
                            time.sleep(.3)

                        resume = not resume # Toggle resume command
                elif pos[0] > labels[0]['pos'][0] - 30 and pos[0] < labels[0]['pos'][0] + 30:
                    if pos[1] > labels[0]['pos'][1] - 10 and pos[1] < labels[0]['pos'][1] + 10:
                        return
                #time.sleep(300)

            update_screen()
if __name__ == "__main__":
    for pin in [17, 22, 23, 27, 19, 26]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_cb, bouncetime=300)

    start_time = time.time()
    update_screen()
    event_loop()

    l_motor.stop()
    r_motor.stop()
    _quit()


