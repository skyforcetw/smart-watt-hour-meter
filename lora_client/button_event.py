# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

BUTTON_PIN = 18
# LED_PIN = 23
button_status = False

def my_callback(channel):
	button_status = not button_status
    print('按下按鈕')
    # GPIO.output(LED_PIN, GPIO.HIGH)
    # time.sleep(0.1)
    # GPIO.output(LED_PIN, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=my_callback, bouncetime=250)

try:
    print('按下 Ctrl-C 可停止程式')
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()
	
# 一個按鍵控制RPi_Cam_Web_Interface, 可以透過wifi簡單看到鏡頭角度
# 但是cam web開下去應該會搶到 定時read電錶的拍照功能, 要看一下衝突會發生甚麼事情=>沒事
# lora_cliet必須支援即時讀取電錶的功能                          