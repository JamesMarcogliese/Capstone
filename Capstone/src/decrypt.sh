#!/bin/sh

pmount /dev/sda1 /media/usb0        			#Mounts USB
pmount /dev/mmcblk0p1 /media/sdcard			#Mount SD

if [ $? -ne 0 ]; then               			#Check if mount was successful
    echo "Mounting Failed!"
    exit
fi

if [ -z "$(find /media/usb0 -type f -name "pudeVol")" ] 	#Check if volume already exists
then  
    echo "Encrypted volume not found!"
    exit
fi


