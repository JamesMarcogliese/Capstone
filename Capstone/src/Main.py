'''
Created on Aug 24, 2014

@author: James
'''
#!/usr/bin/python
import time
import Adafruit_CharLCD as LCD
from matrix_keypad import BBb_GPIO
import Adafruit_BBIO.UART as UART
import FPS
import test_raw

UART.setup("UART2")
fps = FPS.FPS_GT511C3()
fps.open()

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

def digit(): # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 

def enrollID():
    fps.UseSerialDebug = True
    if (fps.GetEnrollCount() == 19):
        lcd.message('Device at maximum\ncapacity. Please\ndelete users.')
        time.sleep(3.0)
        break
    lcd.clear()
    fps.SetLED(True)							
    lcd.message('Press finger on\nscanner to check if\nalready enrolled.')
    ID = verify()
    if (ID != 200 and ID != 20):
        lcd.clear()
        lcd.message('You are already\nenrolled. Returning\nto main.')
        time.sleep(3.0)
        break
    else:
        for i in range(0,19):
            if (fps.CheckEnrolled(i) == False):
                ID = i		  
    lcd.message('Press finger to\nEnroll.')
    fps.EnrollStart(ID)
    while (fps.IsPressFinger() == False):
        time.sleep(0.1)
    bret = fps.CaptureFinger(True)
    iret = 0
    if (bret != False):
        lcd.clear()
        lcd.message('Remove finger.\n')
        fps.Enroll1()
        while (fps.IsPressFinger() == True):
            time.sleep(0.1)
        lcd.clear()
        lcd.message('Press same finger again.\n')
        while (fps.IsPressFinger() == False):
            time.sleep(0.1)
        bret = fps.CaptureFinger(True)
        if (bret != False):
            lcd.clear()
            lcd.message('Remove finger.\n')
            fps.Enroll2()
            while (fps.IsPressFinger() == True):
                time.sleep(0.1)
            lcd.clear()
            lcd.message('Press same finger\nyet again.\n')
            while (fps.IsPressFinger() == False):
                time.sleep(0.1)
            bret = fps.CaptureFinger(True)
            if (bret != False):
                lcd.clear()
                lcd.message('Remove finger.\n')
                iret = fps.Enroll3()
                if (iret == 0):
                    lcd.clear()
                    lcd.message('Enrollment\nSuccessful!')
                else:
                    lcd.clear()
                    lcd.message('Enroll failed.\nPlease try again.\n')
                    time.sleep(3.0)       
            else:
                lcd.message('Failed to capture\nthird finger.')  
        else:
            lcd.message('Failed to capture\nsecond finger.')
    else:
        lcd.message('Failed to capture\nfirst finger.')
    fps.SetLED(False)
    
def encrypt():
    print "encrypt"
    
def decrypt():
    print "decrypt"
    
def deleteID():                
    lcd.clear() 
    lcd.message('Place finger on\nscanner to\nverify ID.') 
    uID = verify()
    lcd.clear()
    if(uID == 200 or uID == 20):
        lcd.message('ID was not found!')
        time.sleep(3.0)
        break
    lcd.message('Delete ID?\n"*" for Yes & "#" for No')
    keyPress = digit()
    if(keyPress == "*"):
        fps.DeleteID(uID)
        lcd.clear()
        lcd.message('ID has been deleted!')
        time.sleep(3.0)
        break
    else: 
        lcd.message('Returning to Menu.')
        time.sleep(3.0)
        break

def verify():
    while (fps.IsPressFinger() == False):
        time.sleep(0.1)
    bret = fps.CaptureFinger(False)
    if (bret != False):
        lcd.clear()            
        lcd.message('Remove finger.\n')
    ID = fps.Identify1_N()
    return ID
    
#MAIN

while True:
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

  
