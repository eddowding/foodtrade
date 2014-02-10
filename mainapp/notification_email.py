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
SERVER = 'localhost' #put Server = localhost for local connection
PORT = 27017
DB_NAME = 'foodtrade'
table_name = 'notification'

# USERNAME = 'roshan'
# PASSWORD = 'bpDf..fdwexFI12'
#..................Server Settings............................
import smtplib
import json

class Email():
    def __init__ (self):
        pass

    def send_mail(self, to, subject, message):
        sender = 'brishi98@gmail.com'
        passwd = 'DS3yEW4HdOzqHGXOiXGPkg'

        server = smtplib.SMTP('smtp.mandrillapp.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender, passwd)

        template_content = {"template_content": [
        {
            "name": "title",
            "content": "<h2>Your Order is Complete</h2>"
        },
        {
            "name": "main",
            "content": "We appreciate your business. Your order information is below."
        }
    ]}
    

        body = '\r\n'.join([
                            'To: %s' % to,
                            # # 'From: %s' % sender,
                            'X-MC-Template: %s' % "foodtrade-master|main",
                            # 'X-MC-Metadata: %s' % json.dumps(template_content),
                            'Subject: %s' % subject,
                            '', message
                            ])

        try:
            server.sendmail(sender, [to], body)
            server.quit()
            return True
        except:
            server.quit()
            return False

def aggregrate_all(conditions={}):
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    # db.authenticate(USERNAME, PASSWORD)

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
    # db.authenticate(USERNAME, PASSWORD)
    notices = get_all_notification_to_send()

    full_result_set = notices[0]
    for eachMessageList in full_result_set['full_result_set']:
        notification_to_user = str(eachMessageList['notification_to'])
        
        to = db.userprofile.find({'username':notification_to_user})
        json_doc = json.dumps(list(to),default=json_util.default)
        # to_email = json.loads(json_doc)[0]['email']

        subject = 'You have message in your Foodtrade Inbox.'

        count = 0
        message_body = ''
        for eachMessage in eachMessageList['results']:
            count += 1
            message_body = message_body + str(count) + '. ' + eachMessage['notification_message'].split('.')[0] + '.\n\t'
        #print message_body, '\n\n\n'

        email_obj = Email()
        # print to_email
        # if to_email == 'ed@foodtrade.com':
        # to_email = 'brishi98@gmail.com'
        print email_obj.send_mail(to_email, subject, message_body)
send_daily_email()
