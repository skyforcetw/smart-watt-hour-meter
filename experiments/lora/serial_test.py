import serial
import time

ser = serial.Serial('/dev/serial0',4800)

print ser.name          # check which port was really used

for x in range(0,10):
    print(x)
    ser.write("hello")      # write a string
    time.sleep(1)

ser.close()             # close port
