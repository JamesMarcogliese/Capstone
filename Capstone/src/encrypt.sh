#!/bin/sh

pmount /dev/sda1 /media/usb0        			#Mounts USB

if [ $? -ne 0 ]; then               			#Check if mount was successful
    echo "USB Mounting Failed!"
    exit
fi

pmount /dev/mmcblk0p1 /media/sdcard			#Mount SD
if [ $? -ne 0 ]; then               			#Check if mount was successful
    echo "SDcard Mounting Failed!"
    exit
fi


if [ -n "$(find /media/usb0 -type f -name "pudeVol")" ] #Check if volume already exists
then  
    echo "Encrypted volume already exists!"
    exit
fi

shopt -s dotglob                                        #Move files to microSD (includes hidden files)
mv /media/usb0/* /media/sdcard  				

usbsize="$(blockdev --getsize64 /dev/sda)" 		#Calculate usb size (total size - 20Mb) then insert it into the below vol creation command 
volsize=`expr $usbsize - 20000000`

truecrypt -t --volume-type=Normal -c /media/usb0/pudeVol --size=$volsize --encryption=AES --hash=SHA-1 --password=password --filesystem=AUTO -k "" --random-source=/dev/urandom --quick 		
							#Create TC volume

truecrypt -t /media/usb0/pudeVol /home/ubuntu/bin/pudeVol --password=password -k "" --protect-hidden=no 
							#Mount TC volume
mv /media/sdcard/* /home/ubuntu/bin/pudeVol		#Move all files back onto encrypted volume

truecrypt -t -d /home/ubuntu/bin/pudeVol 		#Unmounts TC volume

cp /bin/TCSripts/* /media/usb0 				#Moves accessibility scripts onto USB

pumount /media/usb0 					#Unmount USB
pumount /media/sdcard					#Unmount SDcard

