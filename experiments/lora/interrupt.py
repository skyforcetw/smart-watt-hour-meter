# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO  #引入RPi.GPIO库
import time

def auxEventHandler (pin):
    if GPIO.input(pin):     # if port 25 == 1  
        print "Rising edge detected"  
    else:                  # if port 25 != 1  
        print "Falling edge detected"  

def main():
	GPIO.setmode(GPIO.BCM)
	pin_aux = 18
	GPIO.setup(pin_aux, GPIO.IN)
	GPIO.add_event_detect(pin_aux,GPIO.BOTH)
	GPIO.add_event_callback(pin_aux,auxEventHandler)

	try:
		while(1):
			time.sleep(0.1)
		
	finally:
		GPIO.cleanup()
		
if __name__=="__main__":
    main()