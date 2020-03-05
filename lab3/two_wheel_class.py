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
class PMotor:
    interval = 0.02

    idle = 0.0015
    r_max = 0.0017
    f_max = 0.0013

    pwm = ''
    
    def __init__(self, pin): 
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 1 / self.interval)
        self.pwm.start(self.idle / (self.idle + self.interval) * 100)

    def set(self, high):
        f = 1 / (high + self.interval)
        pw = high
        dc = high / (high + self.interval) * 100
        print "Setting Motor -> F: {}\tPW: {}\tDC: {}".format(f, pw, dc)  
    
        self.pwm.ChangeDutyCycle(dc)


    def stop(self):
        self.pwm.stop()

if len(sys.argv) > 1:
    frequency = int(sys.argv[1])

motor = PMotor(5)

motor_speed = motor.r_max
motor.set(motor_speed)

while 1:
    pass

for i in range (10):
   time.sleep(3)
   motor_speed += (motor.f_max - motor.idle) / 10
   motor.set(motor_speed)

motor_speed = motor.idle
setPMotor(motor, motor_speed)
for i in range (10):
   time.sleep(3)
   motor_speed += (motor.r_max - motor.idle) / 10
   motor.set(motor_speed)

motor.stop()
_quit()
