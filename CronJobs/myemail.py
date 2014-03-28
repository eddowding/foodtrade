import mandrill 
import pymongo
from pymongo import Connection
from settingslocal import *

table_name = 'notification'

class Email():
    def __init__ (self):        
        self.conn = Connection(LOCAL_SERVER,REMOTE_MONGO_PORT)
        self.db = self.conn[REMOTE_MONGO_DBNAME]
        self.db.authenticate(REMOTE_MONGO_USERNAME, REMOTE_MONGO_PASSWORD)
        self.table_name = 'emailbacklogs'

    def save_backlogs(self,doc):
        self.db.emailbacklogs.insert(doc)          

    def send_mail(self, subject, template_content=[{}], to = [{}]):
        # sender = 'ed@foodtrade.com'
        # passwd = 'NwotnhPk1Nprc6OX0Wq6vA'
        md = mandrill.Mandrill('NwotnhPk1Nprc6OX0Wq6vA')
        mes = mandrill.Messages(md)

        message ={
            'auto_html': False,
            'auto_text': False,
            'to':to,
            'from_email':'no-reply@foodtrade.com', 
            'from_name':'FoodTrade', 
            'important':'true',
            'track_click':'true',
            'subject':subject,
        }

        template_content = template_content
        self.save_backlogs({'message':message, 'template_content':template_content})
        mes.send_template('foodtrade-master', template_content, message)