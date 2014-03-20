#!/bin/bash

cd /backup
mkdir $(date +%F)
cd $(date +%F)
mongodump -uftroot -pftroot --db foodtrade
mysqldump -u root -proot foodtrade > foodtrade.sql 
cd ..
zip -r $(date +%F).zip $(date +%F)/
rsync /backup/$(date +%F).zip foodtrade@ftstaging.cloudapp.net:~/backups
rm -r $(date --date="1 day ago" +%F)
rm  $(date +%F).zip