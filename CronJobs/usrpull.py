#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import os
import sys
import time, datetime

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from settings_local import *
from friends import Friends
    
start_time = datetime.datetime.now() - datetime.timedelta(1)
start_time = time.mktime(start_time.timetuple())
start_time = int(start_time)

user_profile_obj = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
users = user_profile_obj.get_all_friends_and_register_as_user(start_time)
        
        
# def solve_errors():
#     te = TwitterError()
#     twitter_errors = te.get_unsolved_error('cron')

#     '''Solve all previous errors'''
#     for eachError in twitter_errors:    
#         '''Make Profile for all the friends who have location'''
#         next_cursor = eachError['next_cursor']
#         if eachError['user_type'] =='friends':
#             users = get_friends(eachError['username'], int(eachError['next_cursor']), 'friends')
#         else:
#             users = get_friends(eachError['username'], int(eachError['next_cursor']), 'followers')
#         try:
#             while(next_cursor !='0'):
#                 next_cursor = users['next_cursor']
#                 for eachFriend in users['users']:
#                     '''Register this user'''
#                     register_user_to_mongo(eachFriend)
#                 if next_cursor != 0:
#                     if eachError['user_type'] =='friends':    
#                         users = get_friends(eachError['username'], next_cursor, 'friends')
#                     else:
#                         users = get_friends(eachError['username'], next_cursor, 'followers')
            
#             '''Normal Flow Update Error Status to Solved'''        
#             twitter_err_obj = TwitterError()
#             twitter_err_obj.save_error({'username':eachError['username'],'error_solve_stat':'false', 'error_type':'cron'}, 
#                 {'error_solve_stat':'true'})
#         except:
#             '''If error occurs save in errors'''
#             twitter_err_obj = TwitterError()
#             if eachError['user_type'] =='friends':
#                 twitter_err_obj.save_error({'username':eachError['username'],'error_type':'cron',
#                     'next_cursor_str':next_cursor, 'error_solve_stat':'false','user_type':'friends'})
#             else:
#                 twitter_err_obj.save_error({'username':eachError['username'],'error_type':'cron',
#                     'next_cursor_str':next_cursor, 'error_solve_stat':'false','user_type':'followers'})