#!/bin/bash

sudo -i
cd /backups
unzip $(date +%F)
cd $(date +%F)
cd dump
mongorestore foodtrade/
mysql -u root -proot foodtrade < foodtrade.sql 
cd ..
logout 


