# William Nunez, wsn8, Yan Zheng, yz2626, Lab2, wed, 2/19
# Modified video control to use callbacks instead of /polling of GPIO

import RPi.GPIO as GPIO
import time
import subprocess # For interrupt

GPIO.setmode(GPIO.BCM)

first_btn = 17
second_btn = 22
third_btn = 23
fourth_btn = 27
fifth_btn = 19
sixth_btn = 26

GPIO.setup(first_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(second_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(third_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fourth_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fifth_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sixth_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Open fifo program for editing

# callbacks
def GPIO17_callback(channel):
		print "Falling edge detected on first button"
def GPIO22_callback(channel):
		print "Falling edge detected on second button"
def GPIO23_callback(channel):
		print "Falling edge detected on third button"
def GPIO19_callback(channel):
		print "Falling edge detected on fifth button"
def GPIO26_callback(channel):
		print "Falling edge detected on sixth button"

#def GPIO22
# Main part of program
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO19_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)

time.sleep(10)

# GPIO.wait_for_edge(fourth_btn, GPIO.FALLING)
# print "Falling edge on button 4 detected"
# fd.write("quit")
# fd.flush()

# Clean up
GPIO.cleanup()



