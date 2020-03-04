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

pwm_pin = 5
GPIO.setup(pwm_pin, GPIO.OUT)

frequency = 60
dc = 50

if len(sys.argv) > 1:
    frequency = int(sys.argv[1])

blink = GPIO.PWM(pwm_pin, frequency)
blink.start(dc)

raw_input("Hit Enter to quit\n")

quit_cb(quit_button)
