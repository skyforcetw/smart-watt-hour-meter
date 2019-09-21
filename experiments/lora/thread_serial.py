# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:46:15 2019

@author: skyforce.shen
"""

#!/usr/bin/python

import serial
import threading
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)
    
port = '/dev/serial0'
baud = 4800
connected = False
serial_port = serial.Serial(port, baud, timeout=120)
signal.signal(signal.SIGINT, keyboardInterruptHandler)


    
def handle_data(data):
    if len(data):
        print(data)

def read_from_port(ser):
    print 'test0'
    while not connected:
        print 'test1'
        #serin = ser.read()
        connected = True
        

        while True:
           print 'test2'
           reading = ser.readline().decode(errors='replace')
           # reading = ser.read()
           handle_data(reading)


print 'main'
thread = threading.Thread(target=read_from_port, args=(serial_port))
thread.start()