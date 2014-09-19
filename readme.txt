
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
=>mysql -uroot -proot
=>drop database foodtrade;
=>create database foodtrade;
=>exit;
Inside the extracted folder where the backup file lies type
=>mysql -uroot -proot foodtrade < foodtrade.sql
Go to the dump folder and in terminal type
=>mongorestore -uftroot -pftroot foodtrade/

#########DO NOT TRY
=>mongo -u ftroot  foodtrade -p --eval "db.dropDatabase();"


Read server data to the local computer
===========================================================
1. Go to the terminal and type:-

	scp foodtrade@ftstaging.cloudapp.net:~/backups/2014-06-12.zip .

2. Then enter the password for ssh of foodtrade




To access server without password 
=================================================================================================
For live:
cat ~/.ssh/id_rsa.pub | ssh kathmandu@foodtradelite.cloudapp.net "cat >> ~/.ssh/authorized_keys"

For Staging server:
cat ~/.ssh/id_rsa.pub | ssh foodtrade@ftstaging.cloudapp.net "cat >> ~/.ssh/authorized_keys"


You will be prompted to enter password. Enter password and its done. :)