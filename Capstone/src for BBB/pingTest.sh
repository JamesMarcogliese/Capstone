#!/bin/bash

#target=$1

count=$( ping -c 1 $hostAddress | grep icmp* | wc -l )

if [ $count -eq 0 ]
then

    echo "Host is not Alive! Try again later.."
    return 1
else

    echo "Yes! Host is Alive!"
    return 2
fi
return
