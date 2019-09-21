# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:43:05 2019

@author: skyforce.shen
"""

import RPi.GPIO as GPIO  #引入RPi.GPIO库
import serial
import time

port = '/dev/serial0'
baud = 4800
pin_aux = 18
pin_md1 = 17
pin_md0 = 27

def setup():
    GPIO.setmode(GPIO.BCM) 

    GPIO.setup(pin_aux, GPIO.IN)
    GPIO.setup(pin_md1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pin_md0, GPIO.OUT, initial=GPIO.LOW)
    # 打开串口
    ser = serial.Serial(port, baud)
    
def loop():
    while True:
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)
            ser.write(recv)
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)

def main():
    setup()
    loop()
     
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()