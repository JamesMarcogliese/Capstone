#!/bin/sh
mkdir -p /media/usb0
mkdir -p /media/sdcard
pmount /dev/sda1 /media/usb0        				#Mounts USB
if [ $? -ne 0 ]; then               				#Check if mount was successful
    echo "Mounting Failed!"
    return 1
fi

pmount /dev/mmcblk0p1 /media/sdcard				#Mount SD
if [ $? -ne 0 ]; then               				#Check if mount was successful
    echo "SDcard Mounting Failed!"
    return 2
fi

if [ -z "$(find /media/usb0 -type f -name "pudeVol.tc")" ] 	#Check if volume already exists
then  
    echo "Encrypted volume not found!"
    pumount /media/usb0 					#Unmount USB
    pumount /media/sdcard
    return 3
fi

timeVal="5"
status="Decrypting"
sudo python appUpdate.py $time $status $user

truecrypt -t -m=nokernelcrypto /media/sdcard/pudeVolTemp.tc /media/sdcard/pudeVolTempDir --password=91238913 -k "" --protect-hidden=no --filesystem=ntfs							#Mounts temp storage SD card
								#Mounts usb TC volume
truecrypt -t -m=nokernelcrypto /media/usb0/dist/pudeVol.tc ~/bin/pudeVol --password=$password -k "" --protect-hidden=no --filesystem=ntfs

shopt -s dotglob                                        	#Move files out from volume to microSD (includes hidden files)
mv ~/bin/pudeVol/* /media/sdcard/pudeVolTempDir/

truecrypt -t -d /media/usb0/dist/pudeVol.tc				#Unmounts volume

rm -rf /media/usb0/*						#Delete all contents of USB (includes encrypted volume and scripts)

mv /media/sdcard/pudeVolTempDir/* /media/usb0			#Move all files back to USB from SDCARD

truecrypt -t -d							#Unmount SDCARD

pumount /media/usb0 						#Unmount USB
pumount /media/sdcard						#Unmount SDcard

timeVal2="0"
status="Decryption Complete"
sudo python appUpdate.py $time $status $user
return 0
