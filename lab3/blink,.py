///////////////    Quit Button Setup    ////////////////////////////////
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

quit_button = 17
GPIO.setup(quit_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quit_cb(channel):
		print "Quit Button Pressed"
    exit(0)

GPIO.add_event_detect(quit_button, GPIO.FALLING, callback=quit_cb, bouncetime=300)


//////////////// Actual code starts from here  //////////////////////
import time
import sys

pwm_pin = 5
GPIO.setup(pwm_pin, GPIO.OUT)

frequency = 30
dc = 50


blink = GPIO.PWM(GPIO_pin, frequency)
blink.start(dc)

raw_input("Hit any key to quit")
