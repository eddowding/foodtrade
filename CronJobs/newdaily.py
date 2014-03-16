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
from UserProfile import UserProfile    

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
            baseurl = "http://foodtrade.com/send-newsletter/" + str(substype.lower())+ "?username=" + str(eachUser['username']) + "&code=11foodtradeESRS22"
            response = urllib2.urlopen(baseurl)

