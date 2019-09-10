# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:43:05 2019

@author: skyforce.shen
"""

import RPi.GPIO as GPIO  #引入RPi.GPIO库
import serial

GPIO.setmode(GPIO.BCM) 

pin_aux = 18
pin_md1 = 23
pin_md0 = 24

GPIO.setup(pin_aux, GPIO.IN)
GPIO.setup(pin_md1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_md0, GPIO.OUT, initial=GPIO.LOW)

# 打开串口
ser = serial.Serial("/dev/serial0", 4800)
print(ser.name) 
ser.write(b'123\n')
ser.flush()
ser.close()



GPIO.cleanup()