# -*- coding: utf-8 -*-
import serial  # 引用pySerial模組
# import RPi.GPIO as GPIO  #引入RPi.GPIO库
import lora_setting as lora
import time

def set_airspeed(speed):
    ok = False
    if speed=='0.3':
        print 'set_airspeed 0.3'
        lora.set_airspeed(0)
        ok = True
    elif speed=='1.2':
        print 'set_airspeed 1.2'
        lora.set_airspeed(1)
        ok = True
    elif speed=='2.4':
        print 'set_airspeed 2.4'
        lora.set_airspeed(2)
        ok = True
    elif speed=='4.8':
        print 'set_airspeed 4.8'
        lora.set_airspeed(3)
        ok = True
    elif speed=='9.6':
        print 'set_airspeed 9.6'
        lora.set_airspeed(4)
        ok = True        
    elif speed=='19.2':
        print 'set_airspeed 19.2'
        lora.set_airspeed(5)
        ok = True        
        
    return ok
    
def set_tx_power(power):
    ok = False
    
    if power=='0':
        print 'power 0'
        lora.set_tx_power(0)
        ok = True
    elif power=='1':
        print 'power 1'
        lora.set_tx_power(1)
        ok = True
    elif power=='2':
        print 'power 2'
        lora.set_tx_power(2)
        ok = True
    elif power=='3':
        print 'power 3'
        lora.set_tx_power(3)
        ok = True    
    return ok

def parse_command(command):
    tokens=command.split(' ');
    if tokens[0] =='#':
        if tokens[1]=='air':
            ser.writelines('OK1\n')
            org_air_speed = lora.get_airspeed()
            
            if set_airspeed(tokens[2]) :
                lora.store_to_sram()
                # lora.load_setting()
                # lora.print_setting()

                if negotiation():
                    print 'negotiation OK'
                else:
                    print 'negotiation NG'
                    lora.set_airspeed(org_air_speed)
                    lora.store_to_sram()
            else:
                print 'wrong air command'
            
        elif tokens[1]=='power':
            ser.writelines('OK1\n')
            org_tx_power = lora.get_tx_power()
            
            if set_tx_power(tokens[2]) :
                lora.store_to_sram()

                if negotiation():
                    print 'negotiation OK'
                else:
                    print 'negotiation NG'
                    lora.set_tx_power(org_tx_power)
                    lora.store_to_sram()
            else:
                print 'wrong power command'
                
            
    elif tokens[0] == '$':
        ok = False
        
        if tokens[1]=='air':
            ok = set_airspeed(tokens[2])          
        elif tokens[1]=='power':
            ok = set_tx_power(tokens[2])
        elif tokens[1]=='load':
            setting = lora.print_setting()
            ser.writelines(setting)
            ser.write('\n')
        if ok :
            lora.store_to_sram()
            # lora.reset()             
    
    elif tokens[0] == 'echo':
        ser.writelines(tokens[1])
        ser.write('\n')
    # print(command ,' ',tokens)
    
def negotiation():    
    # ser.writelines('OK1\n')
    #改設定
    #改好 回傳OK2
    # lora.normal()
    time.sleep(1)
    lora.normal()
    # time.sleep(1)
    # ser.writelines('OK2\n')
    # ser.writelines('OK2\n')
    # ser.writelines('OK2\n')
    ser.writelines('OK2\n')
    print 'send OK2'
    
    ser.timeout = 9
    result = 0
    data_raw = ser.readline()  # 讀取一行
    data_raw = data_raw.strip();
    
    # 成功
    if data_raw == 'OK3':
        print 'recv OK3'
        result = 1
 
    ser.timeout = None
    return result
 
port = '/dev/serial0'
baud = 9600
ser = serial.Serial(port, baud)   # 初始化序列通訊埠
 
pin_aux = 18
pin_md1 = 17
pin_md0 = 27  

lora.begin(ser,pin_md0,pin_md1,pin_aux)

lora.print_setting()
lora.normal()

print 'wait for lora tx...'
try:
    while True:
        while ser.in_waiting:          # 若收到序列資料…
            data_raw = ser.readline()  # 讀取一行
            data_raw = data_raw.strip();
            print 'lora rx: ', data_raw
            parse_command(data_raw)
            
 
except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件
    print('再見！')
    

