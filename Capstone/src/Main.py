'''
Created on Aug 24, 2014

@author: James
'''
#!/usr/bin/python
#import Adafruit_BBIO.GPIO as GPIO
import math
import time
import Adafruit_CharLCD as LCD
from matrix_keypad import BBb_GPIO

lcd_rs        = 'P8_8'
lcd_en        = 'P8_10'
lcd_d4        = 'P8_18'
lcd_d5        = 'P8_16'
lcd_d6        = 'P8_14'
lcd_d7        = 'P8_12'
lcd_backlight = 'P8_7'
lcd_columns = 20
lcd_rows    = 4
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

kp = BBb_GPIO.keypad(columnCount = 4)

def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 

def enroll():
    print "enroll"
def encrypt():
    print "encrypt"
def decrypt():
    print "decrypt"
def delete():                
    print "delete"  
#if __name__ == '__main__': 
loop = 1   
while (loop):
    #lcd.clear()
    #lcd.message('  PUD-E MAIN MENU\n1-ENROLL   2-ENCRYPT\n3-DECRYPT  4-DELETE\n  <SELECT OPTION>')
    
    print "Please enter a option: "
 
# Getting digit 1, printing it, then sleep to allow the next digit press.
    d1 = digit()
    print d1
    time.sleep(1.0)
    if d1 == 1:
	enroll()
    elif d1 == 2:
	encrypt()
    elif d1 == 3:
	decrypt()
    elif d1 == 4:
	delete();
    elif d1 > 4 or d1 == 0 or d1 == "A" or d1 == "B" or d1 == "C" or d1 == "D" or d1 == "E" or d1 == "F":
	print "fuck you"
    
#pass

            
          
                
 
    
