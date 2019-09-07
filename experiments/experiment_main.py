# -*- coding: utf-8 -*-
import cv2
from norma_image import normal_with_log
import find_circle
import circle_to_rect
#import math
import time

start = time.time()

debug = 1
use_binary = 1
dump_image = 0
rect_w_extend = 2
output_dir = './output/'

if debug:
    gray_image = cv2.imread('../images/normal.png',0)
else:
    image = cv2.imread('../images/640x480.png',0)
    gray_image = normal_with_log(image)
    cv2.imwrite(output_dir+'normal.png',gray_image)
#    gray_image = cv2.cvtColor(normal_image, cv2.COLOR_BGR2GRAY)  #convert to gray
    

circles = find_circle.find(gray_image)
max_r =circles.T[2].max()
no = 0


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
    print(i, " ", value)    
	
    if dump_image:
        crop_image = rect_images[1]
        cv2.imwrite(output_dir+'square-%d.png' %(no),rect_image)
        cv2.imwrite(output_dir+'crop-%d.png' %(no),crop_image)    

    no+=1	
    
print  time.time() - start