
== How to install on localhost ==
1. create database foodtrade;
2. delete mainapp/fixture/my_json.json
3. go to mainapp/userdata/ --> run --> python data-gen.py
4. python manage.py syncdb
5. python manage.py loaddata mainapp/fixtures/social_account.yaml
