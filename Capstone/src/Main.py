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

UART.setup("UART2")
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

def digit(): # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 

def enrollID():
    fps.UseSerialDebug = True
    lcd.clear()
    if (fps.GetEnrollCount() == 19):
        lcd.message('Device at maximum\ncapacity. Please\ndelete users.')
        time.sleep(5.0)
        return
    fps.SetLED(True)							
    lcd.message('Press finger on\nscanner to check if\nalready enrolled.')
    ID = verify()
    if (ID != 20):
        lcd.clear()
        lcd.message('You are already\nenrolled. Returning\nto main.')
        time.sleep(5.0)
        return
    else:
        lcd.clear()
        lcd.message('ID not found!')
        for i in range(1,19):
            if (fps.CheckEnrolled(i) == False):
                ID = i
                break	
    lcd.clear()
    time.sleep(5)	  
    lcd.message('Press finger to\nEnroll.')
    fps.EnrollStart(ID)
    while (fps.IsPressFinger() == False):
        time.sleep(1)
    bret = fps.CaptureFinger(True)
    if (bret != False):
        lcd.clear()
        lcd.message('Remove finger.\n')
        num = fps.Enroll1()
        while (fps.IsPressFinger() == True):
            time.sleep(1)
        lcd.clear()
        lcd.message('Press same finger\n again.')
        while (fps.IsPressFinger() == False):
            time.sleep(1)
        bret = fps.CaptureFinger(True)
        if (bret != False):
            lcd.clear()
            lcd.message('Remove finger.\n')
            num = fps.Enroll2()
            while (fps.IsPressFinger() == True):
                time.sleep(1)
            lcd.clear()
            lcd.message('Press same finger\nyet again.\n')
            while (fps.IsPressFinger() == False):
                time.sleep(1)
            bret = fps.CaptureFinger(True)
            if (bret != False):
                lcd.clear()
                lcd.message('Remove finger.\n')
                time.sleep(3.0)
                iret = fps.Enroll3()
                if (iret == 0):
                    lcd.clear()
                    lcd.message('Enrollment\nSuccessful!')
                    time.sleep(5)
                else:
                    lcd.clear()
                    lcd.message('Enroll failed.\nPlease try again.\n')
                    time.sleep(5.0)       
            else:
                print "Failed to capture third finger."
        else:
            print "Failed to capture second finger."
    else:
        print "Failed to capture first finger."
    
def encrypt():
    print "encrypt"
    
def decrypt():
    print "decrypt"
    
def deleteID():
    fps.SetLED(True)            
    lcd.clear() 
    lcd.message('Place finger on\nscanner to\nverify ID.') 
    uID = verify()
    print uID
    lcd.clear()
    if(uID == 200 or uID == 20):
        lcd.message('ID was not found!')
        time.sleep(5.0)
        return
    lcd.message('ID was found!\nDelete ID?\n"*" for Yes\n"#" for No')
    keyPress = digit()
    if(keyPress == "*"):
        fps.DeleteID(uID)
        lcd.clear()
        lcd.message('ID has been deleted!')
        time.sleep(5.0)
        return
    else: 
        lcd.clear()
        lcd.message('Returning to Menu.')
        time.sleep(5.0)
        return

def verify():
    while (fps.IsPressFinger() == False):
        time.sleep(1)
    bret = fps.CaptureFinger(False)
    if (bret != False):
        lcd.clear()            
        lcd.message('Remove finger.\n')
    ID = fps.Identify1_N()
    lcd.clear()
    return ID
    
#MAIN

while True:
    lcd.clear()
    fps.SetLED(False)
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

  
