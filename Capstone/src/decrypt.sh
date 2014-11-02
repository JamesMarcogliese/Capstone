#!/bin/sh

pmount /dev/sda1 /media/usb0        				#Mounts USB
pmount /dev/mmcblk0p1 /media/sdcard				#Mount SD

if [ $? -ne 0 ]; then               				#Check if mount was successful
    echo "Mounting Failed!"
    exit
fi

if [ -z "$(find /media/usb0 -type f -name "pudeVol")" ] 	#Check if volume already exists
then  
    echo "Encrypted volume not found!"
    exit
fi
								#Mounts TC volume
truecrypt -t /media/usb0/pudeVol /home/ubuntu/bin/pudeVol --password=password -k "" --protect-hidden=no 

shopt -s dotglob                                        	#Move files out from volume to microSD (includes hidden files)
mv /home/ubuntu/bin/pudeVol/* /media/sdcard

rm -rf example							#Delete all contents of USB (includes encrypted volume and scripts)

mv /media/sdcard/* /media/usb0					#Move all files back to USB from SDCARD

pumount /media/usb0 						#Unmount USB
pumount /media/sdcard						#Unmount SDcard
