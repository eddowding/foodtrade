# import imp
# search = imp.load_source('search', 'C:\Users\Roshan Bhandari\Desktop\project repos\foodtrade\mainapp\classes\Search.py')
import os
import sys

APP_ROOT = os.path.realpath('..')
APP_ROOT = APP_ROOT.replace('\\','/')

CLASS_PATH = APP_ROOT + '/mainapp/classes'
SETTINGS_PATH = APP_ROOT + '/foodtrade'


sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from MongoConnection import MongoConnection
from Search import Search

class UserProfile():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'useruid')

    def get_all_profiles(self, status):
        users = []
        if status == 'None':
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}})/15)+ 1
        else:
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':status})/15)+ 1
        for i in range(0,user_pages_count, 1):
            if status == 'None':
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}}, pageNumber = int(i+1))
            else:    
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':status}, pageNumber = int(i+1))
            for eachUser in pag_users:
                users.append(eachUser)
        return users


def send_newsletter(substype):
    substype = substype.capitalize()
    user_profile_obj = UserProfile()
    
    if substype == 'Daily':
        users = user_profile_obj.get_all_profiles('Daily')
    elif substype == 'Weekly' or substype == 'None':
        users = user_profile_obj.get_all_profiles(substype)
    elif substype == 'Monthly':
        users = user_profile_obj.get_all_profiles('Monthly')
    count = 0
    for eachUser in users:
        if len(eachUser['email'])>0:
            import urllib2
            baseurl = "http://localhost:8000/send-newsletter/" + str(substype.lower())+ "?username=" + str(eachUser['username']) + "&code=11foodtradeESRS22"
            response = urllib2.urlopen(baseurl)

