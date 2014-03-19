
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
=> db.addUser({"user":"ftroot","pwd":"ftroot","roles":["readWrite", "dbAdmin"]})
=> db.auth({"user":"ftroot","pwd":"ftroot","roles":["readWrite", "dbAdmin"]})
=> use foodtrade
=> db.addUser({"user":"ftroot","pwd":"ftroot","roles":["readWrite", "dbAdmin"]})
