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
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
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
        subject = 'You have message in your Foodtrade Inbox.'
        to_user = json.dumps(list(to_user),default=json_util.default)
        to_user = json.loads(to_user)
        #print to_user[0]['email']
        message_body = ''
        message_body = '<table><tr style="background-color:green;"><td style="width:30%;">From</td><tdstyle="width:50%;">Activity</td><td style="width:20%;">Action</td></tr>'
        for eachMessage in eachMessageList['results']:
            message_body = message_body + '<tr>'
            message_body = message_body + '<td style="width:30%;">@' + eachMessage['notifying_user'] + '</td><td style="width:50%;">' + eachMessage['notification_message'].split('.')[0] + '</td>'
            message_body = message_body + '<td style="width:20%;"><a href="http://foodtrade.com/inbox">reply</a></td>'
            message_body = message_body + '</tr>'
        email_obj = Email()
        message_body = message_body + '</table>'
        email_obj.send_mail(
            subject, 
            [{'name':'main', 'content':message_body},{'name':'inbox','content':'''<p>Please check your inbox for more details by clicking the following link</p><p><a href="http://foodtrade.com/inbox">My Foodtrade Inbox. </a></p>'''}], 
            [{'email':to_user[0]['email']}])
send_daily_email()