# -*- coding: utf-8 -*-
import serial  # 引用pySerial模組
import lora_setting as lora

port = '/dev/serial0'
baud = 9600
ser = serial.Serial(port, baud)   # 初始化序列通訊埠
 
pin_aux = 18
pin_md1 = 17
pin_md0 = 27  

lora.begin(ser,pin_md0,pin_md1,pin_aux)


if True :
    flash = True
    data = [0xC0 if flash else 0xC2,0,0,0x18,0x17,0x41]
    for x in range(1,6):
        # data[x] = lora_setting[x]
        print data[x]
    lora.sleep()
    write_len = ser.write(data)    
    ser.timeout = 3
    recv = ser.readline()  # 讀取一行    
    print recv
    ser.timeout = 0

lora.load_setting()
lora.print_setting()
# lora.set_airspeed(0)
# lora.print_setting()
# lora.store_to_flash()
lora.reset()
