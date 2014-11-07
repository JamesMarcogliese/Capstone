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
import subprocess
import sqlite3
import random

try:
    db = sqlite3.connect('Pude.db')
    cursor = db.cursor()
except Exception as e:
    print e
    
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

def digit():                                                                # Loop while waiting for a keypress
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
    uID = verify()
    if (uID != 20):
        lcd.clear()
        lcd.message('You are already\nenrolled. Returning\nto main.')
        time.sleep(5.0)
        return
    else:
        lcd.clear()
        lcd.message('ID not found!')
        for i in range(0,19):
            if (fps.CheckEnrolled(i) == False):
                uID = i
                break	
    lcd.clear()
    time.sleep(3)	  
    lcd.message('Press finger to\nEnroll.')
    status = fps.EnrollStart(uID)
    if(status != 0):
        print "Error starting enrollment!"
        lcd.clear()
        lcd.message('Error starting\nenrolling!')
        time.sleep(5.0)
        return
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
        lcd.message('Press same finger\nagain.')
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
                    pwd = random.randrange(10000000, 99999999)
                    try:
                        cursor.execute('INSERT INTO Users(ID, PASSWORD) VALUES(?,?)', (uID, pwd))
                        db.commit() 
                    except Exception as e:
                        db.rollback()
                        print e
                    time.sleep(5)
                    return
                else:
                    lcd.clear()
                    lcd.message('Enroll failed.\nPlease try again.\n')
                    time.sleep(5.0)       
            else:
                print "Failed to capture third finger."
                lcd.clear()
                lcd.message('Failed to capture\nthird finger.')
                time.sleep(5.0)
                return
        else:
            print "Failed to capture second finger."
            lcd.clear()
            lcd.message('Failed to capture\nsecond finger.')
            time.sleep(5.0)
            return
    else:
        print "Failed to capture first finger."
        lcd.clear()
        lcd.message('Failed to capture\nfirst finger.')
        time.sleep(5.0)
        return
    
    
def encrypt(): #SHOW PASSWORD
    fps.SetLED(True)            
    lcd.clear() 
    lcd.message('Place finger on\nscanner to\nverify ID.') 
    uID = verify()

    ret = subprocess.call("./encrypt.sh")
    if(ret !=0):
        print "Error with encrypt.sh!"
    
def decrypt():
    fps.SetLED(True)            
    lcd.clear() 
    lcd.message('Place finger on\nscanner to\nverify ID.') 
    uID = verify()
    
    ret = subprocess.call("./decrypt.sh")
    if(ret !=0):
        print "Error with decrypt.sh!"
    
def deleteID():
    fps.SetLED(True)            
    lcd.clear() 
    lcd.message('Place finger and\nhold on scanner to\nverify ID.') 
    uID = verify()                                                              #Checks ID
    print uID
    lcd.clear()
    if(uID == 200 or uID == 20):
        lcd.message('ID was not found!')
        time.sleep(3.0)
        return
    lcd.message('ID was found!\nDelete ID?\n"*" for Yes\n"#" for No')
    keyPress = digit()
    if(keyPress != "*"):                                                        #Any other response will redirect user to Main
        lcd.clear()
        lcd.message('Returning to Menu.')
        time.sleep(3.0)
        returnt
    else:
        time.sleep(3.0)
        lcd.clear()
        lcd.message('Are you sure?\n"*" for Yes\n"#" for No')
        keyPress = digit()
    if(keyPress == "*"):
        status = fps.DeleteID(uID)
        if (status == True):
            try:
                cursor.execute('DELETE FROM Users WHERE ID = ?', (uID,))           #DB deletes user
                db.commit()
            except Exception as e:
                db.rollback()
                print e
                print "DB Delete action failed!"
            lcd.clear()
            lcd.message('ID has been deleted!')
            time.sleep(5.0)
            return
        else: 
            print "Error deleting ID!"
            lcd.clear()
            lcd.message('Error deleting ID!\nAction aborted!')
            time.sleep(5.0)
            return
    else: 
        lcd.clear()
        lcd.message('Returning to Menu.')
        time.sleep(5.0)
        return
        
def checkPwd():
    fps.SetLED(True)            
    lcd.clear() 
    lcd.message('Place finger on\nscanner to\nverify ID.') 
    uID = verify()                                                              #Checks ID
    print uID
    lcd.clear()
    if(uID == 200 or uID == 20):
        lcd.message('ID was not found!')
        time.sleep(5.0)
        return
    lcd.clear() 
    lcd.message('ID found!\nPassword will be\ndisplayed for 8s.') 
    time.sleep(5.0)
    cursor.execute('SELECT Password FROM Users WHERE ID = ?',(uID,))             #Retrieves password from DB
    pwd = cursor.fetchone()
    newpwd = str(pwd)
    lcd.clear()
    print pwd
    lcd.message('Password is:\n')
    lcd.message(newpwd[3:11])
    del pwd
    time.sleep(8.0)
    return
    
def verify():                                                                   #Generic function to check for ID
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
    lcd.message('  PUD-E MAIN MENU\n1-Enroll   2-Encrypt\n3-Decrypt  4-Delete\n5-Check Password')
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
    elif d1 == 5:
        checkPwd()
    elif d1 > 5 or d1 == 0 or d1 == "*" or d1 == "#":
        pass

  
