#!/bin/sh

sudo /sbin/route add default gw 192.168.7.1
sudo bash -c "echo "nameserver 8.8.8.8" >> /etc/resolv.conf"
