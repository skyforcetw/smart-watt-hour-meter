import cv2
from norma_image import normal_with_log
import find_circle
import circle_to_square
import math

debug = 1
use_binary = 1
dump_image = 1
output_dir = './output/'

if debug:
    normal_image = cv2.imread('../images/normal.png')
else:
    image = cv2.imread('../images/640x480.png')
    normal_image = normal_with_log(image)
    cv2.imwrite(output_dir+'normal.png',normal_image)
    
gray_image = cv2.cvtColor(normal_image, cv2.COLOR_BGR2GRAY)  #convert to gray
circles = find_circle.find(gray_image)
max_r =circles.T[2].max()
no = 0


for i in circles[0]:
    i[2]=max_r
    h_start = ((max_r*2)>>3)*3 #3/8開始取
    
    square_images = circle_to_square.get_cartesian_image(gray_image,i[0],i[1],i[2],0,2,h_start)
    square_image = square_images[0]
#    crop_image = square_images[1]
#    cv2.imwrite('crop-%d.png' %(no),crop_image)        
	
    height, width = square_image.shape[:2]
    square_image = square_image[h_start:height, :]
    square_image = cv2.equalizeHist(square_image)
	
    if use_binary:
        square_image = cv2.adaptiveThreshold\
        (square_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,159,35)

	
    value = circle_to_square.get_current_value(square_image)
    value = find_circle.parse_value(value,no%2==0,1==no)
    print(i, " ", value)    
	
    if dump_image:
        cv2.imwrite(output_dir+'square-%d.png' %(no),square_image)
        cv2.imwrite(output_dir+'crop-%d.png' %(no),square_images[1])    

    no+=1	