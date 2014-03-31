import pprint
import datetime
import time
import pymongo
from pymongo import Connection
import json
from bson import BSON
from bson import json_util
import re
from settingslocal import *

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from Email import Email

def aggregrate_all(conditions={}):
    conn = Connection(LOCAL_SERVER,REMOTE_MONGO_PORT)
    db = conn[REMOTE_MONGO_DBNAME]
    db.authenticate(REMOTE_MONGO_USERNAME, REMOTE_MONGO_PASSWORD)    
    all_doc =  db.notification.aggregate(conditions)['result']
    json_doc = json.dumps(list(all_doc),default=json_util.default)
    json_doc = json_doc.replace("$oid", "id")
    json_doc = json_doc.replace("_id", "uid")
    return json.loads(str(json_doc))

def get_all_notification_to_send():
    aggregation_pipeline = []
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    aggregation_pipeline.append({"$match":{'notification_time':{'$gt':time.mktime(yesterday.timetuple())}}})
    aggregation_pipeline.append({"$match":{'notification_type':'Added Food'}})
    aggregation_pipeline.append({
        "$group":
            {"_id": "$notification_to", 
            "results":
            {'$push':{
            "notification_time":"$notification_time", 
            "notification_to":"$notification_to", 
            "notification_type":"$notification_type", 
            "notifying_user":"$notifying_user", 
            "notification_message":"$notification_message"}
            }
            }
        })
    aggregation_pipeline.append({
        '$group':{
            '_id':"$notification_to",
            'full_result_set':
                {'$push':
                    {'notification_to':'$_id','results':'$results'}
                }
            }})
    return aggregrate_all(aggregation_pipeline)


def send_daily_email():
    conn = Connection(LOCAL_SERVER,REMOTE_MONGO_PORT)
    db = conn[REMOTE_MONGO_DBNAME]
    db.authenticate(REMOTE_MONGO_USERNAME, REMOTE_MONGO_PASSWORD)
    notices = get_all_notification_to_send()
    try:
        full_result_set = notices[0]
    except:
        return
    for eachMessageList in full_result_set['full_result_set']:
        notification_to_user = str(eachMessageList['notification_to'])
        to_user = db.userprofile.find({'username':str(notification_to_user)})
        to = db.userprofile.find({'username':notification_to_user})
        json_doc = json.dumps(list(to),default=json_util.default)
        subject = 'You have message in your FoodTrade inbox'
        to_user = json.dumps(list(to_user),default=json_util.default)
        to_user = json.loads(to_user)
        #print to_user[0]['email']
        message_body = ''
        message_body = '\
        <table cellpadding="2" cellspacing="0">\
            <tr style="background-color:#6C7F40;">\
                <td style="width:30%; color: #fff;">From</td>\
                <td style="width:50%; color: #fff;">Activity</td>\
                <td style="width:20%; color: #fff;">Action</td>\
            </tr>'
        for eachMessage in eachMessageList['results']:
            message_body = message_body + '<tr>'
            message_body = message_body + '<td style="width:30%; font-size: 11px; color: #444;">@' + eachMessage['notifying_user'] + '</td><td style="width:50%; font-size: 11px; color: #444;">' + eachMessage['notification_message'].split('.')[0] + '</td>'
            message_body = message_body + '<td style="width:20%; font-size: 11px; color: #444;">\
            <a href="http://foodtrade.com/inbox">reply</a></td>'
            message_body = message_body + '</tr>'
        email_obj = Email()
        message_body = message_body + '</table>'
        email_obj.send_mail(
            subject, 
            [
                {'name':'main', 'content':message_body},
                {'name':'inbox','content':'''<p>Please check your inbox for more details by clicking the following link</p><p><a href="http://foodtrade.com/inbox">My Foodtrade Inbox. </a></p>'''}
            ], 
            [{'email':to_user[0]['email']}])
send_daily_email()