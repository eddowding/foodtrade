#!/bin/bash

sudo -i
cd /backup
mkdir $(date +%F)
cd $(date +%F)
mongodump
mysqldump -u root -proot foodtrade > foodtrade.sql 
cd ..
zip -r $(date +%F).zip $(date +%F)/
rm -r $(date --date="1 day ago" +%F)
rm  $(date +%F).zip
logout 
rsync /home/backups/newdump.zip foodtrade@ftstaging.cloudapp.net:~/backups

