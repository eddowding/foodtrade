#!/bin/bash

#database backup
sudo -i
cd /home/backups/
cd d1 
sudo rm -r dump
cd ..
sudo cp d2 -r d1
cd d2 
sudo rm -r dump
cd ..
sudo cp d3 -r d2
cd d3
sudo rm -r dump
mongodump
mysqldump -u root -proot foodtrade > foodtrade.sql 

#run daily email sending script
#python /srv/www/foodtrade-env/foodtrade/mainapp/notification-email.py

