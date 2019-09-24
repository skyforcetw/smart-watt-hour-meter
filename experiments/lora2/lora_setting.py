# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO  #引入RPi.GPIO库
import serial  # 引用pySerial模組

pin_md1 = 17
pin_md0 = 27  
pin_aux = 18

port = '/dev/serial0'
baud = 4800
ser = serial.Serial(port, baud)   # 初始化序列通訊埠
status = 'unknow'

def auxEventHandler (pin):
    if GPIO.input(pin):     # if port 25 == 1  
        print "Rising edge detected"  
    else:                  # if port 25 != 1  
        print "Falling edge detected"  

    
def begin(_ser,_pin_md0 ,_pin_md1,_pin_aux):
    ser=_ser
    pin_md0=_pin_md0
    pin_md1=_pin_md1
    pin_aux=_pin_aux
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(pin_md1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pin_md0, GPIO.OUT, initial=GPIO.LOW)   
    
    GPIO.setup(pin_aux, GPIO.IN)
    GPIO.add_event_detect(pin_aux,GPIO.BOTH)
    GPIO.add_event_callback(pin_aux,auxEventHandler)
    
    normal()
    load_setting()
    # status = 'normal'

def sleep():
    global status
    status = 'sleep'
    GPIO.output(pin_md1, GPIO.HIGH)
    GPIO.output(pin_md0, GPIO.HIGH)
    
def normal():
    global status
    status = 'normal'
    GPIO.output(pin_md1, GPIO.LOW)
    GPIO.output(pin_md0, GPIO.LOW)
    
lora_setting = []
    
def load_setting():
    # set_lora_normal()
    org_status = status
    print 'org status: ' , status
    
    sleep()
    
    ser.baudrate = 9600
    data = [193,193,193]
    ser.write(data)

    ser.timeout = 3
    recv = ser.readline()  # 讀取一行
    
    length = len(recv)
    index = 0
    global lora_setting
    empty = len(lora_setting) ==0
    
    if 0 != length:
        for c in recv:
            if empty :
                lora_setting.append(ord(c))
            else:
                lora_setting[index]=ord(c)

            index+=1
    else:
        # print 'no recv'
        lora_setting=[]
 
    ser.timeout = None
    
    if 'normal' == org_status:
        print 'back to normal'
        normal()
    
def set_airspeed(speed):
    if 0 == len(lora_setting):
        return
    
    setted = (lora_setting[3] & 0xF8) | (speed);
    lora_setting[3] = setted
    
def print_setting():
    if 0 == len(lora_setting):
        print 'no lora setting'
        return
    for s in lora_setting:
        print s
 