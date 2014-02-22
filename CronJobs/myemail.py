import mandrill 
import pymongo
from pymongo import Connection
#..................Server Settings............................
SERVER = 'localhost'
PORT = 27017
DB_NAME = 'foodtrade'
table_name = 'notification'
#..................Server Settings............................
class Email():
    def __init__ (self):        
        self.conn = Connection(SERVER,PORT)
        self.db = conn[DB_NAME]
        self.table_name = 'emailbacklogs'
        self.db_object.create_table(self.table_name,'_id')

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
