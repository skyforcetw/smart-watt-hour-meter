# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 00:13:02 2019

@author: skyfo
"""
import cv2
import numpy as np
import math

def sort_circles(circles,sort_index):
    circles = np.uint16(np.around(circles))
    y = circles.T[sort_index]
    y = y.flatten()
    index = np.argsort(y) 
    circles = circles[0:1,index,]
    return circles

def parse_value(val,ccw,last_no):
    val = 10.0-val if ccw else val
    round_val = round(val)
    if (round_val - val) <=0.1 and 0 == last_no:
        val += 0.1

    val = val if last_no else math.floor(val)
    val = val - 10 if val >=10 else val
    return val

def find(img,radius = 128):
    height, width = img.shape[:2]
    
    max_radius = int( radius * 1.1)
    min_radius = int(radius * 0.9)
    circle_distance = int(min_radius*2 )
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,circle_distance,
                    param1=50,param2=30,minRadius=min_radius,maxRadius=max_radius)
						
    circles = sort_circles(circles,0)
    return circles
	# max_r =circles.T[2].max()
	
    # no=0
    
    # for i in circles[0]:
        # i[2]=max_r
        
        # h_start = ((max_r*2)>>3)*3 #3/8開始取
        
        # cartesian_images = cartesian.get_cartesian_image(img,i[0],i[1],i[2],0,2,h_start)
        # cartesian_image = cartesian_images[0]
        # crop_image = cartesian_images[1]
        # cv2.imwrite('crop-%d.png' %(no),crop_image)        
        
        # height, width = cartesian_image.shape[:2]
        # cartesian_image = cartesian_image[h_start:height, :]
        # cartesian_image = cv2.equalizeHist(cartesian_image)
        
        # if use_binary:
            # cartesian_image = cv2.adaptiveThreshold(cartesian_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,127,20)
 
        
        # value = cartesian.get_current_value(cartesian_image)
        # value = parse_value(value,no%2==0,1==no)
        # print(i, " ", value)    
        
        # if dump_image:
            # cv2.imwrite('cartesian-%d.png' %(no),cartesian_image)
            # cv2.imwrite('crop-%d.png' %(no),cartesian_images[1])    
 
        # no+=1	