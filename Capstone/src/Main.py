'''
Created on Aug 24, 2014

@author: James
'''
#!/usr/bin/python
#import Adafruit_BBIO.GPIO as GPIO
import math, time, sys
import Adafruit_CharLCD as LCD
from matrix_keypad import BBb_GPIO
import FPS
from test_raw import *

fps = FPS.FPS_GT511C3()

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
kp = BBb_GPIO.keypad(columnCount = 3)
loop = 1
ID = 0
def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 

def enrollID():
    fps.UseSerialDebug = True
	enrollCount = fps.GetEnrollCount()
    lcd.clear()
    fps.SetLED(True)							#check IDS and check if exists already
	lcd.message("Press finger on\nscanner to check ID")
     while (fps.IsPressFinger() == False)
	  time.sleep(0.1)
      bret = fps.CaptureFinger(True)
	  if (bret != False) 
        lcd.clear()
        lcd.message('Remove finger\n')
	ID = fps.Identify1_N()
	if (ID != 200)
	  lcd.clear()
	  lcd.message('You are already\nenrolled. Select\nanother option.\nReturning to main.')
	  time.sleep(3.0)
	  break
	else
	  for i in range(0,19):
        if (fps.CheckEnrolled(i) == False)
          ID = i		  
	lcd.message('Press finger to\nEnroll')
	fps.EnrollStart()
    while (fps.IsPressFinger() == False)
	  time.sleep(0.1)
      bret = fps.CaptureFinger(True)
	  iret = 0
	  if (bret != False) 
        lcd.clear()
        lcd.message('Remove finger\n')
		fps.
    lcd.clear()
    lcd.message('Press same finger again\n')
    lcd.clear()
    lcd.message('Remove finger\n')
    lcd.clear()
    lcd.message('Press same finger\nyet again\n')
    lcd.clear()
    lcd.message('Remove finger\n')
    lcd.clear()
	fps.SetLED(False)
def encrypt():
    print "encrypt"
def decrypt():
    print "decrypt"
def deleteID():                
    print "delete" 
 

#MAIN
import Adafruit_BBIO.UART as UART
UART.setup("UART2")

while (loop):
    lcd.clear()
    lcd.message('  PUD-E MAIN MENU\n1-Enroll   2-Encrypt\n3-Decrypt  4-Delete\n  <SELECT OPTION>')
    d1 = digit()
    print d1
    if d1 == 1:
	enrollID()
    elif d1 == 2:
	encrypt()
    elif d1 == 3:
	decrypt()
    elif d1 == 4:
	deleteID()
    elif d1 > 4 or d1 == 0 or d1 == "*" or d1 == "#":
	pass

  
