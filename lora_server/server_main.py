# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 23:36:17 2019

@author: skyfo
"""
from __future__ import print_function
import serial
import time
import struct

baud = 9600
port = 'com9'

ser = serial.Serial(port, baud)  # open first serial port
 
enter_binary = "***Enter binary mode***"
leave_binary = "***Leave binary mode***"

    
def main():
    binary_mode = False
    filename = 'store.jpg'
    binary_count = 0
    
    while True:
        if binary_mode:
            line = ser.read()
            binary_count+=1
        else:
            # 获得接收缓冲区字符
            line = ser.readline()
            line = line.strip('\r\n')
        
        if line == enter_binary:
            binary_mode = True
            f = open ( filename , mode = 'wb' )
            print ('in binary')
            continue
            
            
        if binary_count>=3968:
            binary_count=0
            binary_mode = False 
            f.close()
            print ('done', end='\n')
            continue
            
        if binary_mode:
            for x in range(0,len(line)):
                v = ord(line[x])
                f.write(struct.pack("B", v))
#                hex_str = format(v, 'x')
#                print (hex_str,' ', end='')
#                print (hex(v),' ', end='')
#            print ('', end='\n')
            print ('.', end='')
        else:
            print(line)
            
#        print(line)
        # 清空接收缓冲区
#        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
