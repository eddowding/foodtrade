#!/bin/bash
cd ~/backups
sudo unzip $(date +%F)
cd $(date +%F)
cd dump
sudo mongo foodtrade --eval "db.dropDatabase()"
sudo mongorestore foodtrade/
cd ..
sudo mysql -u root -proot foodtrade < foodtrade.sql 
cd ..