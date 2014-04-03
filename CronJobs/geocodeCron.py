#!/usr/bin/env python
# encoding: utf-8

import sys

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

# SETTINGS_PATH = 'C:/Users/Roshan Bhandari/Desktop/foodtrade/foodtrade'
# CLASS_PATH = 'C:/Users/Roshan Bhandari/Desktop/foodtrade/mainapp/classes'

sys.path.insert(0, CLASS_PATH)
sys.path.insert(1, SETTINGS_PATH)

from settingslocal import *
from UserProfile import UserProfile

userprofile_obj = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
userprofile_obj.geocode_all_antartic_users()