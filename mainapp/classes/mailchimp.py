import mailchimp
from mainapp.mc_utils import *
from pymongo import Connection
from MongoConnection import MongoConnection

class MailChimp():
    """This class is used to make api calls to the MailChimp"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'mailchimp'
        self.db_object.create_table(self.table_name,'_id')

    def save_mailchimp_response(self, doc):
        self.db_object.update_upsert(self.table_name, doc['data_sent'], doc)

    def subscribe(self, doc):
        try:
            try:
                first, last = doc['name'].split(' ')[0], doc['name'].split(' ')[1]
            except:
                first, last = doc['name'].split(' ')[0], ''
            m = get_mailchimp_api()
            response = m.lists.subscribe(list_id, email = {'email':str(doc['email'])}, 
                merge_vars = {"FNAME":str(first),"LNAME":str(last),
                "groupings": [{"name": "Foodtrade Group","groups": [str(doc["sign_up_as"])]}],
                "mc_location":{"latitude":str(doc["latlng"]["coordinates"][1]),"longitude":str((doc["latlng"]["coordinates"][1]))}},
                update_existing=True, send_welcome=True, replace_interests=True)
            self.save_mailchimp_response({'data_sent':doc, 'response':response})
            return {'status':1}

        except mailchimp.ListAlreadySubscribedError:
            return {'status':0,'message':'Already subscribed'}


