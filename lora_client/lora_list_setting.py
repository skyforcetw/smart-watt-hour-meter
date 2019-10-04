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
 

lora.load_setting()
lora.print_setting()
 