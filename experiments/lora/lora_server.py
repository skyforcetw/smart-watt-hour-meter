# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:05:07 2019

@author: skyfo
"""
 
import serial
import time

baud = 4800
port = 'com3'


pin_aux = 18
pin_md1 = 17
pin_md0 = 27
ser = serial.Serial(port, baud)  # open first serial port
 
    
def main():
     
    
    while True:
        # 获得接收缓冲区字符
        line = ser.readline()
        line = line.strip('\r\n')
        print(line)
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()    