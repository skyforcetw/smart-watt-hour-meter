# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO  #引入RPi.GPIO库
import serial  # 引用pySerial模組
import time

pin_md1 = 17
pin_md0 = 27  
pin_aux = 18

port = '/dev/serial0'
baud = 9600
ser = serial.Serial(port, baud)   # 初始化序列通訊埠
status = 'unknow'
wait_after_change_mode = 0.4

def auxEventHandler (pin):
    if GPIO.input(pin):
        print "Rising edge detected"       
    else:
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
    # GPIO.add_event_callback(pin_aux,auxEventHandler)
    
    normal()
    load_setting()
    # status = 'normal'

def sleep():
    global status
    status = 'sleep'
    GPIO.output(pin_md1, GPIO.HIGH)
    GPIO.output(pin_md0, GPIO.HIGH)
    time.sleep(wait_after_change_mode)
    
def normal():
    global status
    status = 'normal'
    GPIO.output(pin_md1, GPIO.LOW)
    GPIO.output(pin_md0, GPIO.LOW)
    time.sleep(wait_after_change_mode)

before_status = 'unknow'
# before_baudrate = 9600

def before_setting():
    global before_status
    # global before_baudrate
    
    before_status = status
    print 'org status: ' , status
    sleep()
    # before_baudrate = ser.baudrate
    # ser.baudrate = 9600
    
def after_setting():
    if 'normal' == before_status:
        normal()
    # ser.baudrate = before_baudrate
    
lora_setting = []
    
def load_setting():
    before_setting()
    
    data = [0xC1,0xC1,0xC1]
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
        lora_setting=[]
 
    ser.timeout = None
    
    after_setting()
    
def reset():
    before_setting()
    
    data = [0xC3,0xC3,0xC3]
    ser.write(data)
    wait_recv()
    
    after_setting()
    
def wait_recv():
    ser.timeout = 3
    recv = ser.readline()  # 讀取一行    
    print 'recv: ',recv
    ser.timeout = 0
    
def set_airspeed(speed):
    if 0 == len(lora_setting):
        return
    
    setted = (lora_setting[3] & 0xF8) | (speed);
    print 'setted: ',setted
    lora_setting[3] = setted
    
def set_tx_power(power):
    if 0 == len(lora_setting):
        return
    
    setted = (lora_setting[5] & 0xFC) | (power);
    lora_setting[5] = setted    
    
def print_setting():
    if 0 == len(lora_setting):
        print 'no lora setting'
        return
    
    setting =''
    for s in lora_setting:
        # print s
        setting +=' '+str(s)
    print 'lora setting: ',setting
        
def store_to_sram():
    before_setting()
    
    data = [0xC2,0,0,0,0,0]
    for x in range(1,5):
        data[x+1] = lora_setting[x]
    write_len = ser.write(data)    
    # print 'write_len: ',write_len
    
    wait_recv()
    
    after_setting()
 