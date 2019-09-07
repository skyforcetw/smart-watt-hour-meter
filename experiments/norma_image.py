# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 23:56:40 2019

@author: skyfo
"""
import cv2
import numpy as np
import math

def normal_with_log(image):
	lut = np.zeros(256,np.uint8 )#创建空的查找表
	offset = 25
	lut[0] = 0

	for gray0 in range(1,256):
		gray = (255.0-offset)/255*gray0 + offset
		normal = gray/255.0*10
		log_normal = math.log(normal,10)
		log_255 = int(round(255 * log_normal))
		lut[gray0] = log_255
#		print gray0 ," ",normal," ",log_normal," ",log_255

	result = cv2.LUT(image, lut)
	return result
 