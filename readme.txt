
== How to install on localhost ==


1. create database foodtrade;
# mysql -uroot -p
# drop database foodtrade
# create database foodtrade;

2. delete mainapp/fixture/my_json.json

3. go to mainapp/userdata/ --> run --> python data-gen.py

4. python manage.py syncdb

5. python manage.py loaddata mainapp/fixtures/social_account.yaml

6. python manage.py loaddata mainapp/fixtures/my_json.json



#### To set user in mongodb

=> mongo
=> use admin
=> db.addUser({"user":"ftroot","pwd":"ftroot","roles":["readWrite", "dbAdmin", "clusterAdmin", "userAdmin"]})
=> db.auth({"user":"ftroot","pwd":"ftroot","roles":["readWrite", "dbAdmin", "userAdmin", "clusterAdmin"]})
=> use foodtrade
=> db.addUser({"user":"ftroot","pwd":"ftroot","roles":["readWrite", "dbAdmin","clusterAdmin", "userAdmin"]})


###### Restoring database from the backup file on local
=>mongo -uftroot -pftroot foodtrade
=>db.dropDatabase()
Extract the backup zip file and inside the folder in terminal type
=>mysl -u root -p root
=>drop database foodtrade;
=>create database foodtrade;
=>exit;
Inside the extracted folder where the backup file lies type
=>mysql -u root -p root foodtrade < foodtrade.sql
Go to the dump folder and in terminal type
=>mongorestore -uftroot -pftroot foodtrade/

#########DO NOT TRY
=>mongo -u ftroot  foodtrade -p --eval "db.dropDatabase();"