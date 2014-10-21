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

#if __name__ == '__main__':    
while (1)
lcd.message('Hello World!')	




#pass

            
                
                
                
                
                
                
                ["else" ":" suite]    
def enroll():

def encrypt():

def decrypt():

def delete():

def verify():

def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 
    
