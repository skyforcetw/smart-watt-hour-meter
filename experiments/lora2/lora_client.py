# -*- coding: utf-8 -*-
import serial  # 引用pySerial模組
# import RPi.GPIO as GPIO  #引入RPi.GPIO库
import lora_setting as lora


def parse_command(command):
    tokens=command.split(' ');
    if tokens[0] =='#':
        if tokens[1]=='air':
            if tokens[2]=='0.3':
                print '0.3'
            elif tokens[2]=='1.2':
                print '1.2'

            if negotiation():
                print 'OK'
            else:
                print 'NG'
            
        elif tokens[1]=='power':
            print 'power'
    
    # print(command ,' ',tokens)
    
def negotiation():    
    ser.writelines('OK1\n')
    #改設定
    #改好 回傳OK2
    ser.writelines('OK2\n')
    
    ser.timeout = 3
    result = 0
    data_raw = ser.readline()  # 讀取一行
    data_raw = data_raw.strip();
    
    # 成功
    if data_raw == 'OK3':
        result = 1
 
    ser.timeout = None
    return result
    


# def set_lora_air():
    # set_lora_normal()
    # set_lora_sleep()
 
port = '/dev/serial0'
baud = 4800
ser = serial.Serial(port, baud)   # 初始化序列通訊埠
 
pin_aux = 18
pin_md1 = 17
pin_md0 = 27  

# GPIO.setmode(GPIO.BCM) 
# GPIO.setup(pin_md1, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(pin_md0, GPIO.OUT, initial=GPIO.LOW)
lora.begin(ser,pin_md0,pin_md1,pin_aux)

# lora.load_setting()
# lora.set_airspeed(4)
lora.print_setting()
# lora.normal();

try:
    while True:
        while ser.in_waiting:          # 若收到序列資料…
            data_raw = ser.readline()  # 讀取一行
            #data_raw = ser.read()  # 讀取一行
            # data = data_raw.decode()   # 用預設的UTF-8解碼
            # print('接收到的原始資料：', data_raw)
            data_raw = data_raw.strip();
            print(data_raw)
            parse_command(data_raw)
            
 
except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件
    print('再見！')
    

