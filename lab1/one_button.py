# This script will send a command to mplayer using the buttons on the pitft and gpio

import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM) # Uses GPIO numbering

# Set inputs
button = 22
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Read input from button for pause

fid = open("/home/pi/lab1/video_fifo","w")
while 1:
    if GPIO.input(button) == GPIO.LOW:
        print("Button 22 has been pressed")
        # Delay for debouncing
        sleep(0.1)
        # Send command to FIFO
        fid.write("pause \r")
        fid.flush()

GPIO.cleanup()


