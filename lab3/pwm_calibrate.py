# William Nunez, Yan Zhang, wsn8, yz2626, wed, 3/4/2020
# Quit Button Setup
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

quit_button = 17
GPIO.setup(quit_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quit_cb(channel):
    GPIO.cleanup()
    exit(0)

GPIO.add_event_detect(quit_button, GPIO.FALLING, callback=quit_cb, bouncetime=300)


# Actual code starts from here
import time
import sys

pwm_pin = 6 
GPIO.setup(pwm_pin, GPIO.OUT)

frequency = 1/0.0215
dc = 1.5/21.5 * 100

if len(sys.argv) > 1:
    frequency = int(sys.argv[1])

p = GPIO.PWM(pwm_pin, frequency)
p.start(dc)

raw_input("Hit Enter to quit\n")

quit_cb(quit_button)
