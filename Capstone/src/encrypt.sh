#!/bin/sh
mkdir -p /media/usb0
mkdir -p /media/sdcard
pmount /dev/sda1 /media/usb0        			#Mounts USB
if [ $? -ne 0 ]; then               			#Check if mount was successful
    echo "USB Mounting Failed!"
    return 1
fi

pmount /dev/mmcblk0p1 /media/sdcard			#Mount SD
if [ $? -ne 0 ]; then               			#Check if mount was successful
    echo "SDcard Mounting Failed!"
    return 2
fi


if [ -n "$(find /media/usb0 -type f -name "pudeVol.tc")" ] #Check if volume already exists
then  
    echo "Encrypted volume already exists!"
    pumount /media/usb0 				#Unmount USB
    pumount /media/sdcard
    return 3
fi

truecrypt -t -m=nokernelcrypto /media/sdcard/pudeVolTemp.tc /media/sdcard/pudeVolTempDir --password=91238913 -k "" --protect-hidden=no --filesystem=ntfs						#Mount encrypted SD card

shopt -s dotglob                                        #Move files to microSD (includes hidden files)
mv /media/usb0/* /media/sdcard/pudeVolTempDir/  				

usbsize="$(blockdev --getsize64 /dev/sda)" 		#Calculate usb size (total size - 20Mb) then insert it into the below vol creation command 
volsize=`expr $usbsize - 30000000`

truecrypt -t --volume-type=Normal -c /media/usb0/pudeVol.tc --size=$volsize --encryption=AES --hash=SHA-1 --password=$password --filesystem=AUTO -k "" --random-source=/dev/urandom --quick 		
							#Create TC volume

truecrypt -t -m=nokernelcrypto /media/usb0/pudeVol.tc /bin/pudeVol --password=$password -k "" --protect-hidden=no --filesystem=none 

mkfs.ntfs -f -L TRUECRYPT /dev/loop1			#Fills empty encrypted volume with NTFS file system

							#Mount TC volume
mv /media/sdcard/pudeVolTempDir/* ~/bin/pudeVol/			#Move all files back onto encrypted volume

truecrypt -t -d 		 			#Unmounts TC volume

cp -r ~/bin/TCScripts/* /media/usb0 			#Moves accessibility scripts onto USB

pumount /media/usb0 					#Unmount USB
pumount /media/sdcard					#Unmount SDcard
return 0
