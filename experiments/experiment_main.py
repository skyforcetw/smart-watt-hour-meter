import cv2
from norma_image import normal_with_log

image = cv2.imread('../images/640x480.png')
normal_image = normal_with_log(image)
cv2.imwrite('normal.png',normal_image)