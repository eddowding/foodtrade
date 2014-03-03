#!/bin/bash

#database backup
sudo -i
cd /home/backup
rm -r dump.*
mkdir dump
cd dump
mongodump
mysqldump -u root -proot foodtrade > foodtrade.sql 
cd ..
zip -r dump.zip dump/*
scp dump.zip foodtrade@ftstaging.com
