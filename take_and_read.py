# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 11:27:04 2019

@author: skyforce
"""

from io import BytesIO
from picamera import PiCamera
import cv2 
import numpy as np
import time
import serial  # 引用pySerial模組

from lora_client import lora_setting as lora
from smart import normal_image
from smart import circle_to_rect
from smart import find_circle

history_dir = './history/'
debug = 1

port = '/dev/serial0'
baud = 9600
ser = serial.Serial(port, baud)   # 初始化序列通訊埠
 
pin_aux = 18
pin_md1 = 17
pin_md0 = 27  

def store_history_image(img):
    format = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
    filename = format + '.jpg'
    cv2.imwrite(history_dir+filename, img)

def capture():
    # Create the in-memory stream
    stream = BytesIO()

    camera = PiCamera()
    camera.start_preview()
    stream.seek(0)
    camera.capture(stream, format='jpeg')
	capture_len = stream.getvalue()
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    
    file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    return img
	
def capture_d():	
	img = cv2.imread('images/im_0012_20190905_225425.jpg')
	return img
    
def circles_to_values(circles,gray_image):

    use_binary = True
    dump_image = True
    output_dir = './images/output/'
    draw_circle = True    
    
    max_r =circles.T[2].max()
    no = 0
    values = []
    circle_centers = []
    
    for i in circles[0]:
        i[2]=max_r
         #3/8開始取
        h_start = ((max_r*2)>>3)*3 

        rect_images = circle_to_rect.get_cartesian_image(gray_image,i[0],i[1],i[2],0,2,h_start)
        rect_image = rect_images[0]
    	
        height, width = rect_image.shape[:2]
        rect_image = rect_image[h_start:height, :]
        rect_image = cv2.equalizeHist(rect_image)
    	
        if use_binary:
            rect_image = cv2.adaptiveThreshold\
            (rect_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,159,35)
    	
        value = circle_to_rect.get_current_value(rect_image)
        value = find_circle.parse_value(value,no%2==0,1==no)
        
        circle_centers.append(i)
        values.append(value)
        
#        print(i, " ", value)    
    	
        if dump_image:
            crop_image = rect_images[1]
            cv2.imwrite(output_dir+'square-%d.png' %(no),rect_image)
            cv2.imwrite(output_dir+'crop-%d.png' %(no),crop_image)
            if draw_circle:
            # draw the outer circle
                cv2.circle(gray_image,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
                cv2.circle(gray_image,(i[0],i[1]),2,(0,0,255),3)
    
        no+=1	
    
    if dump_image:
        cv2.imwrite(output_dir+'circle.png',gray_image)  

    pairs = [circle_centers,values]
    return pairs
#    return values

def tx_values(values):
    lora.begin(ser,pin_md0,pin_md1,pin_aux)

    lora.print_setting()
    lora.normal()

def main():

    print "time : %s" % time.ctime()
    image = capture() if 0 == debug else capture_d()
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    store_history_image(image)
    
    gray_image = normal_image.normal_with_log(image)
    cv2.imwrite('./images/gray.jpg', gray_image)
        # time.sleep( sleep_time )
    circles = find_circle.find(gray_image)
    pairs = circles_to_values(circles,gray_image)
    circle_centers = pairs[0]
    values = pairs[1]
	
    if 2 == len(values):
        print circle_centers
        print values
        tx_values(values)
        
    
if __name__=='__main__':
    main()