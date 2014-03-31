#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import os
import sys
import time, datetime
import MySQLdb

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from MongoConnection import MongoConnection
from TwitterError import TwitterError
from UserProfile import UserProfile
from MySQLConnect import MySQLConnect
from settings_local import *
from twython import Twython
from pygeocoder import Geocoder
from friends import Friends

#mongo -uftroot -pftroot foodtrade
#bgr = pygeocoder.Geocoder('471653599669-qht8a4r1mrhqma4902f1iag4i6if4tuf.apps.googleusercontent.com', 'hU7DLea2DXvkYzoaXhNtkHfF')
# db.userprofile.update( {'address':'Antartica'},{ $set: {'latlng.coordinates.0':-135.10000000000002}},{ multi: true })

def register_user_to_mongo(eachFriend):
    user_profile_obj = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, 
        conn_type='remote', username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
    min_user_id = int(user_profile_obj.get_minimum_id_of_user()[0]['minId']) -1
    data = {
        'is_unknown_profile':'true',
        'recently_updated_by_super_user': 'false', 
        'useruid': int(min_user_id),
        'sign_up_as': str('unclaimed'),
        'type_user': [], 
        'name': eachFriend['name'],
        'email': '', 
        'description': eachFriend['description'],
        'username' : eachFriend['screen_name'],
        'screen_name': eachFriend['screen_name'],
        'profile_img': eachFriend['profile_image_url'],
        'updates': [],
        'foods':[],
        'organisations':[],
        'subscribed':0,
        'newsletter_freq':'Never'
    }
    try:
        location_res = Geocoder.geocode(eachFriend['location'])
        data['address'] = str(location_res)
        data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude) ,float(location_res.latitude)]}
        data['zip_code'] = str(location_res.postal_code)
    except:
        data['address'] = str('Antartica')
        data['latlng'] = {"type":"Point","coordinates":[float(-135.10000000000002) ,float(-82.86275189999999)]}
        data['zip_code'] = str('')
        data['location_default_on_error'] = 'true'

    join_time = datetime.datetime.now()
    join_time = time.mktime(join_time.timetuple())
    data['join_time'] = int(join_time)

    print data['screen_name']
    '''Register User to Mongo'''    
    user_profile_obj.update_profile_upsert({'screen_name':eachFriend['screen_name'],
        'username':eachFriend['screen_name']},data)
    return True

fr = Friends()        
fr.register_all_friends()