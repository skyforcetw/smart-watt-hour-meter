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


# aux_event_callback
def set_aux_callback(callback):

    # aux_event_callback = callback
    GPIO.add_event_callback(pin_aux,callback)
    
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
    print 'recv: ',recv if len(recv) !=0 else 'empty'
    ser.timeout = 0

def get_airspeed():
    if 0 == len(lora_setting):
        return -1
        
    speed = (lora_setting[3] & 0x7)
    return speed
    
def set_airspeed(speed):
    if 0 == len(lora_setting):
        return
    
    setted = (lora_setting[3] & 0xF8) | (speed);
    # print 'setted: ',setted
    lora_setting[3] = setted

def get_tx_power():
    if 0 == len(lora_setting):
        return -1
    power = (lora_setting[5] & 0x3)
    return power
        
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
        setting +=' '+hex(s)
    setting = 'lora setting: '+setting+'; size:'+ format(len(lora_setting))
    print setting
    return setting
        
def store_to_sram():
    store(False)

def store_to_flash():
    store(True) 
        
def store(flash):
    before_setting()
    
    data = [0xC0 if flash else 0xC2,0,0,0,0,0]
    for x in range(1,6):
        data[x] = lora_setting[x]
    write_len = ser.write(data)    
    
    wait_recv()
    
    after_setting()
 