from io import BytesIO
from picamera import PiCamera
import cv2 
import numpy as np
import time

# Create the in-memory stream
stream = BytesIO()
camera = PiCamera()
camera.start_preview()
camera.capture(stream, format='png')
# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)

file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

format = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) 
filename = format + '.png'
cv2.imwrite(filename, img)