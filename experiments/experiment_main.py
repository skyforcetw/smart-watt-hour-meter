# -*- coding: utf-8 -*-
import cv2
from norma_image import normal_with_log
import find_circle
import circle_to_rect
#import math
import time
import numpy as np

start = time.time()

debug = 0
use_binary = 1
dump_image = 1
rect_w_extend = 2
output_dir = './output/'
draw_circle = 1

if debug:
    gray_image = cv2.imread('../images/normal.png',0)
else:
    image = cv2.imread('../images/im_0012_20190905_225425.jpg',0)
#    image = np.uint8(np.around(image))
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #convert to gray
    gray_image = normal_with_log(image)
    cv2.imwrite(output_dir+'normal.png',gray_image)
    
    

circles = find_circle.find(gray_image)
max_r =circles.T[2].max()
no = 0
n=20
kernel = np.ones((n,n),np.uint8)

for i in circles[0]:
    i[2]=max_r
     #3/8開始取
    h_start = ((max_r*2)>>3)*3 
#    h_start = 1
   
    
    rect_images = circle_to_rect.get_cartesian_image(gray_image,i[0],i[1],i[2],0,2,h_start)
    rect_image = rect_images[0]
     
	
    height, width = rect_image.shape[:2]
    rect_image = rect_image[h_start:height, :]
    rect_image = cv2.equalizeHist(rect_image)
	
    if use_binary:
        rect_image = cv2.adaptiveThreshold\
        (rect_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,159,35)

#    rect_image = cv2.morphologyEx(rect_image, cv2.MORPH_OPEN, kernel)
	
    value = circle_to_rect.get_current_value(rect_image)
#    value = circle_to_rect.get_current_value_by_line(rect_image)
    value = find_circle.parse_value(value,no%2==0,1==no)
    print(i, " ", value)    
	
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
print  time.time() - start