# -*- coding: utf-8 -*-
import serial  # 引用pySerial模組
import lora_setting as lora
import RPi.GPIO as GPIO  #引入RPi.GPIO库
import time

busy = False
pin_aux = 18
pin_md1 = 17
pin_md0 = 27  

# def wait_busy():
    # print 'busy'

    # global busy
    # if not busy:
        # while not busy:
            # time.sleep(0.1)
        # return True
    # return False
    
def wait_free():    
    GPIO.wait_for_edge(pin_aux, GPIO.RISING)
    
    
def auxEventHandler (pin):
    global busy
    if GPIO.input(pin):
        # print "Rising edge detected"
        print 'unbusy'
        busy = False
    else:
        # print "Falling edge detected"    
        print 'busy'
        busy = True
        
filename = 'crop-0.jpg'

port = '/dev/serial0'
baud = 9600
ser = serial.Serial(port, baud)   # 初始化序列通訊埠



lora.begin(ser,pin_md0,pin_md1,pin_aux)
lora.normal()

try:

    with open(filename, "rb") as f:
        whole_file = f.read()
        size = len(whole_file)
        size_str = str(size)
        size_str = size_str.zfill(4)
        output = 'bin' + size_str   
        
        print output
        ser.write('\n')
        time.sleep(1)
        ser.writelines(output)
        ser.write('\n')
     
        
        f.seek(0)
        byte = f.read(1)
        ser.write(byte)
     
        send_total_count = 1
        send_count = 1
        
        while byte != "":
            # Do stuff with byte.
            byte = f.read(1)
            ser.write(byte)
            
            send_total_count+=1
            send_count+=1
            if send_count>=255:
                wait_free()
                send_count = 0
            
           
        ser.write('\n')
        ser.writelines(reversed(output))
        ser.write('\n')
        
        print 'total send: ' , send_total_count

except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件    
  