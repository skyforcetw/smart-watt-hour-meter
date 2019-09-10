# -*- coding: utf-8 -*-
import cv2  
import time
import numpy as np

import sys
sys.path.insert(0, '..')  
try:
    from ..smart import normal_image
except ValueError:
    from smart import normal_image
#import find_circle
#import circle_to_rect
#import math


start = time.time()

debug = 1
use_binary = 1
dump_image = 1
rect_w_extend = 2
output_dir = './output/'
draw_circle = 1


 
image = cv2.imread('../images/im_0012_20190905_225425.jpg',0)
 
gray_image = normal_image.normal_with_log(image)
cv2.imwrite(output_dir+'normal.png',gray_image)
print 'done'
 