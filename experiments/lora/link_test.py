# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:43:05 2019

@author: skyforce.shen
"""

import RPi.GPIO as GPIO  #引入RPi.GPIO库
import serial
import time

GPIO.setmode(GPIO.BCM) 

pin_aux = 18
pin_md1 = 17
pin_md0 = 27  

GPIO.setup(pin_aux, GPIO.IN)
GPIO.setup(pin_md1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_md0, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.output(pin_md1, GPIO.LOW)
# GPIO.output(pin_md0, GPIO.LOW)
time.sleep(1)
# 打开串口
ser = serial.Serial('/dev/serial0',4800)

# print ser.name          # check which port was really used
ser.write(time.ctime())
ser.write('\n\r')
# for x in range(0,10):
    # print(x)
    # ser.write(str(x))      # write a string
    # time.sleep(2)

ser.close()             # close port



GPIO.cleanup()
