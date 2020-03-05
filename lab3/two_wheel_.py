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

GPIO.add_event_detect(quit_button, GPIO.FALLING, callback=quit_cb, bouncetime=300)
signal(SIGINT, quit_sig)

# Actual code starts from here
import time
import sys

interval = 0.02

motor_stop = 0.0015
motor_r_max = 0.0017
motor_f_max = 0.0013

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

def setMotorTo(pwm, option):
    if option == 'f':
        setPMotor(pwm, motor_f_max)
    elif option == 'r':
        setPMotor(pwm, motor_r_max)
    elif option == 'i':
        setPmotor(pwm, motor_stop)

if len(sys.argv) > 1:
    frequency = int(sys.argv[1])

leftM_pin = 5
rightM_pin = 6

GPIO.setup(leftM_pin, GPIO.OUT)
GPIO.setup(rightM_pin, GPIO.OUT)

leftM = GPIO.PWM(leftM_pin, 60)
rightM = GPIO.PWM(rightM_pin, 60)

startMotor(leftM)
startMotor(rightM)

raw_input("Press Enter to Stop\n")

motor.stop()
_quit()
