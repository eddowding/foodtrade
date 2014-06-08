#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import os
import sys
import time, datetime
import MySQLdb

# CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
# SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

CLASS_PATH = 'C:/Users/Roshan Bhandari/Desktop/foodtrade/mainapp/classes'
SETTINGS_PATH = 'C:/Users/Roshan Bhandari/Desktop/foodtrade/foodtrade'


sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from MongoConnection import MongoConnection
from TwitterError import TwitterError
from MySQLConnect import MySQLConnect
from settingslocal import *
from twython import Twython
from pygeocoder import Geocoder
from UserProfile import UserProfile

usr = UserProfile()
usr.update_banner_for_all_users()