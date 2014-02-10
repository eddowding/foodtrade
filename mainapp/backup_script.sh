#!/bin/bash

#database backup
cd /home/backups/
cd d1 
rm -r dump
cd ..
cp d2 -r d1
cd d2 
rm -r dump
cd ..
cp d3 -r d2
cd d3
mongodump
mysql -u root -proot foodtrade > foodtrade.sql 

#run daily email sending script
python /srv/www/foodtrade-env/foodtrade/mainapp/notification-email.py

