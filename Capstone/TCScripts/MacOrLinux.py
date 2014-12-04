#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
import os
import getpass
from time import sleep
pass
os.system('clear')
print "PUDE USB SCRIPT"
print " "
print "1: Open encrypted volume"
print "2: Close encrypted volume"
print "3: Exit"
print " "
option = input("Please choose an option:")

if (option == 1):
    version = platform.system()
    if ("Windows" in version):
        os.system('TrueCrypt\TrueCrypt.exe /q background /e /m rm /v "pudeVol.tc"')
    elif ("Linux" in version):
        os.system('clear')
        os.system('u="$USER"')
        os.system('sudo $u mkdir -p ~/truecrypt1')
        os.system('sudo chmod 777 ~/truecrypt1')
        os.system('sudo cp -f ./dist/TrueCrypt/truecrypt /usr/bin/')
        os.system('sudo chmod u+s /usr/bin/truecrypt')
        os.system('sudo chmod 777 ./dist/pudeVol.tc')
        os.system('sudo chown $u:$u /usr/bin/truecrypt')
        p = getpass.getpass("Please enter password to unlock encrypted PUDE volume: ")
        os.environ['code'] = p
        os.system('sudo truecrypt -t --fs-options="uid=1000,gid=1000,umask=0002" ./dist/pudeVol.tc ~/truecrypt1 --password=$code -k "" --protect-hidden=no --filesystem=ntfs-3g')

    elif ("Darwin" in version):
        os.system('clear')
        p = getpass.getpass("Please enter password to unlock encrypted PUDE volume: ")
        os.environ['code'] = p
        os.system('sudo ./dist/TrueCrypt/TrueCrypt.app/Contents/MacOS/TrueCrypt -t --mount ./dist/pudeVol.tc /Volumes/truecrypt1 -k "" --protect-hidden=no -p=“$code”')
    else:
        print "OS not supported, sorry!"

    print "Encrypted Volume is mounted!"
        
    pass
elif (option == 2):
    version = platform.system()
    if ("Windows" in version):
        os.system('TrueCrypt\TrueCrypt.exe /q /d')
    elif ("Linux" in version):
        os.system('truecrypt -d')
    elif ("Darwin" in version):
        os.system('sudo ./dist/TrueCrypt/TrueCrypt.app/Contents/MacOS/TrueCrypt -t -d')     
    else:
        print "OS not supported, sorry!"  
        
    print "Encrypted Volume unmounted!"
    sleep(5)
    pass
else:
    pass
