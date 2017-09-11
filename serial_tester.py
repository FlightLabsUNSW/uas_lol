#!/usr/bin/env python

from time import sleep
import serial

ser = serial.Serial('com4', 9600) # Establish the connection on a specific port

ser.write("m1 on")

ser.close()

'''
counter = 32 # Below 32 everything in ASCII is gibberish
while True:
     counter +=1
     print counter
     ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
     print ser.readline() # Read the newest output from the Arduino
     sleep(.1) # Delay for one tenth of a second
     if counter == 255:
          counter = 32
          #sleep(2)
'''