# -*- coding: utf-8 -*-
import serial  # 引用pySerial模組

filename = '../experiments/output/crop-0.jpg'
# f = open(filename, 'rb')
# data = f.read()
# print size(data)
port = '/dev/serial0'
baud = 9600
ser = serial.Serial(port, baud)   # 初始化序列通訊埠

pin_aux = 18
pin_md1 = 17
pin_md0 = 27  

lora.begin(ser,pin_md0,pin_md1,pin_aux)
lora.normal()


with open(filename, "rb") as f:
    whole_file = f.read()
    size = len(whole_file)
    size_str = str(size)
    # print size.zfill(4)
    size_str = size_str.zfill(4)
    output = 'bin' + size_str   
    
    print output
    ser.writelines(output)
    ser.write('\n')
    # print 'bin'
    # print size_str
    
    # print 'bin'
    # print('%04d' % size)
    
    f.seek(0)
    byte = f.read(1)
    while byte != "":
        # Do stuff with byte.
        byte = f.read(1)

        # ser.write(byte)
       
    ser.write('\n')
    ser.writelines(reversed(output))
    ser.write('\n')