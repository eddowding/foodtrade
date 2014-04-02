#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import os
import sys

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'
sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from friends import Friends

fr = Friends()        
fr.register_all_friends()