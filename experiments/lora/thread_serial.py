# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:46:15 2019

@author: skyforce.shen
"""

import threading
import serial

connected = False
port = '/dev/serial0'
baud = 4800

serial_port = serial.Serial(port, baud)
#serial_port.open()
 
def handle_data(data):
    print(data)

def read_from_port(ser):
#    while not connected:
#        #serin = ser.read()
#        connected = True

        while True:
#           print("test")
           reading = ser.readline().decode()
           handle_data(reading)
           ser.write(b'123\n')
           ser.flush()

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()