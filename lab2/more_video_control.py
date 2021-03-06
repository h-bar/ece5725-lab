import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)



first_btn = 17
second_btn = 22
third_btn = 23
forth_btn = 27
fifth_btn = 19
sixth_btn = 26

GPIO.setup(first_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(second_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(third_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(forth_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fifth_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sixth_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)


fd = open('./video_fifo','w')
while True:
    if GPIO.input(first_btn) == GPIO.LOW:
        print 'Button 17 is pressed'
        fd.write("pause\n")
        fd.flush()
        time.sleep(2)
    elif GPIO.input(second_btn) == GPIO.LOW:
        print 'Button 22 is pressed'
        fd.write("seek 10 0\n")
        fd.flush()
        time.sleep(2)
    elif GPIO.input(third_btn) == GPIO.LOW:
        print 'Button 23 is pressed'
        fd.write("seek -10 0\n")
        fd.flush()
        time.sleep(2)
    elif GPIO.input(forth_btn) == GPIO.LOW:
        print 'Button 27 is pressed'
        fd.write("quit\n")
        fd.flush()
        time.sleep(2)
    elif GPIO.input(fifth_btn) == GPIO.LOW:
        print 'Button 19 is pressed'
        fd.write("seek 30 0\n")
        fd.flush()
        time.sleep(2)
    elif GPIO.input(sixth_btn) == GPIO.LOW:
        print 'Button 26 is pressed'
        fd.write("seek -30 0\n")
        fd.flush()
        time.sleep(2)

fd.close()
GPIO.cleanup()
