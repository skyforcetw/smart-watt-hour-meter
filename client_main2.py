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

history_dir = './history/'
# _15_min = 60 * 15
# _15_sec = 15
# sleep_time = _15_sec

# Create the in-memory stream
stream = BytesIO()
camera = PiCamera()
camera.resolution = (640, 360)

def capture():
    camera.start_preview()
    stream.seek(0)
    camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    
    file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    format = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
    filename = format + '.jpg'
    cv2.imwrite(history_dir+filename, img)
    return img
    
def main():
    # while 1:

    print "time : %s" % time.ctime()
    image = capture()
        # time.sleep( sleep_time )

    
if __name__=='__main__':
    main()