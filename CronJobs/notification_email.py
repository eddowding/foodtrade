import pprint
import datetime
import time
import pymongo
from pymongo import Connection
import json
from bson import BSON
from bson import json_util
import re
#..................Server Settings............................
SERVER = 'localhost'
PORT = 27017
DB_NAME = 'foodtrade'
table_name = 'notification'
#..................Server Settings............................
from myemail import Email

def aggregrate_all(conditions={}):
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    all_doc =  db.notification.aggregate(conditions)['result']
    json_doc = json.dumps(list(all_doc),default=json_util.default)
    json_doc = json_doc.replace("$oid", "id")
    json_doc = json_doc.replace("_id", "uid")
    return json.loads(str(json_doc))

def get_all_notification_to_send():
    aggregation_pipeline = []
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    aggregation_pipeline.append({"$match":{'notification_time':{'$gt':time.mktime(yesterday.timetuple())}}})
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
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    notices = get_all_notification_to_send()

    full_result_set = notices[0]
    for eachMessageList in full_result_set['full_result_set']:
        notification_to_user = str(eachMessageList['notification_to'])
        
        to = db.userprofile.find({'username':notification_to_user})
        json_doc = json.dumps(list(to),default=json_util.default)
        subject = 'You have message in your Foodtrade Inbox.'

        count = 0
        message_body = ''
        for eachMessage in eachMessageList['results']:
            count += 1
            message_body = message_body + str(count) + '. ' + eachMessage['notification_message'].split('.')[0] + '.\n\t'

        email_obj = Email()
        email_obj.send_mail(to_email, subject, message_body)
send_daily_email()
