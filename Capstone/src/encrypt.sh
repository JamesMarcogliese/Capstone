#!/bin/sh

pmount /dev/sda1 /media/usb0        #mounts USB

if [ $? -ne 0 ]; then               #check if mount was successful
    echo "Mounting Failed!"
    exit
fi

if [ -n "$(find /media/usb0 -type f -name "vol")" ] #check if col already exists
then  
    echo "Encrypted volume already exists!"
    exit
fi

#move files to microSD
#calculate usb size (total size - 20Mb) then insert it into the below command under --size
truecrypt -t --volume-type=Normal -c /media/usb0/vol.tc --size=500000000 --encryption=AES --hash=SHA-1 --password=password --filesystem=AUTO -k "" --random-source=/dev/urandom --quick 

truecrypt -t /media/usb0/Vol.tc /home/ubuntu/bin/Vol #Mount TC volume
#Move all files back
truecrypt -t -d /home/ubuntu/bin/Vol #unmounts TC volume
pumount /media/usb0 #unmounts USB


