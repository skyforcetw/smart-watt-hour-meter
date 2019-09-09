# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:06:01 2019

@author: skyforce.shen
"""
import cv2
import numpy as np
import math

def polar_to_cartesian(img_p,w_extend=1,h_start=0):
    shape = img_p.shape
    r = shape[0]
    rows_c = r
    cols_c = r*w_extend
#    img_c = np.zeros((rows_c,cols_c, 1), np.uint8)
    img_c = np.full((rows_c,cols_c, 1),255, np.uint8)

    polar_d = img_p.shape[1]
    polar_r = polar_d/2
    
    delta_r = polar_r * 1.0 / rows_c
    delta_t = 2.0 * math.pi / cols_c
    
    center_polar_x = (polar_d-1)/2.0
    center_polar_y = (polar_d-1)/2.0
    
    theta_p = - math.pi/2.0
    
    for i in range(0,cols_c):
        sin_theta = math.sin(theta_p)
        cos_theta = math.cos(theta_p)
        temp_r=0
        
        for j in range(h_start,rows_c):
            temp_r =delta_r*j
            polar_x = int(round(center_polar_x - temp_r * cos_theta))
            polar_y = int(round(center_polar_y + temp_r * sin_theta))

            polar_x = cols_c-1 if polar_x >=cols_c else polar_x
            polar_y = rows_c-1 if polar_y >=rows_c else polar_y
            polar_x = 0 if polar_x <0 else polar_x
            polar_y = 0 if polar_y <0 else polar_y
            
            img_c[j,i] = img_p[polar_y,polar_x]
#            temp_r+=delta_r
        
        theta_p += delta_t
    
    return img_c

def get_cartesian_image(img,x,y,r,use_binary=1,w_extend=1,h_start=0):
    crop_x = x - r
    crop_y = y - r
    crop_img0 = img[crop_y:crop_y+r*2, crop_x:crop_x+r*2]

    if use_binary:
#        th, crop_img = cv2.threshold(crop_img0,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)    
        th, crop_img = cv2.threshold(crop_img0,100,255,cv2.THRESH_BINARY_INV )    
#        crop_img = cv2.adaptiveThreshold(crop_img0,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,87,10)
    else:
        crop_img = crop_img0   
    
    cartesian = polar_to_cartesian(crop_img,w_extend,h_start)
    return [cartesian,crop_img0]

def get_current_value(img):
    shape = img.shape
    width = shape[1]
    
    sum_of_col = np.sum(img,axis=0)
    max_index = np.argmax(sum_of_col)   
    sum_of_col_flip = np.flip(sum_of_col)
    max_index_flip = np.argmax(sum_of_col_flip) 
    max_index_flip = width-1 - max_index_flip
    
    if max_index != max_index_flip:
        max_index =int(round( (max_index+max_index_flip)/2.0))
    
#    print max_index
    ratio = (1.0- max_index*1.0 / width)*10
    return ratio

def get_current_value_by_line(img):
    height, width = img.shape[:2]
#    shape = img.shape
#    width = shape[1]
    
    max_index = -1
    max_line_length = 0
    for w in range(0, width):
        line_length = 0
        for h in range(height-1,1,-1):
            now_pixel = img[h,w]
            pre_pixel = img[h-1,w]
            if now_pixel == 255 and pre_pixel == 0:
                break
            elif now_pixel == 255 and pre_pixel == 255:
                line_length+=1
        if line_length > max_line_length:
            max_line_length = line_length
            max_index = w

    print max_index
#    sum_of_col = np.sum(img,axis=0)
#    max_index = np.argmax(sum_of_col)       
    ratio = (1.0- max_index*1.0 / width)*10
    return ratio