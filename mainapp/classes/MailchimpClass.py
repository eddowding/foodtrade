#!/usr/bin/env python
# encoding: utf-8

import mailchimp
from pymongo import Connection
from MongoConnection import MongoConnection

class MailChimpClass():
    """This class is used to make api calls to the MailChimp"""
    def __init__(self, list_id = '610c67b4de'):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'mailchimp'
        self.list_id =  list_id
        self.db_object.create_table(self.table_name,'_id')
    
    def get_mailchimp_api(self):
        # return mailchimp.Mailchimp('e9294366710f56f159569b82660f9df3-us3') #your api key here
        return mailchimp.Mailchimp('0a92cdd6b266f6e6f1db98639bfa20e2-us2') #your api key here

    def save_mailchimp_response(self, doc):
        self.db_object.update_upsert(self.table_name, doc['data_sent'], doc)

    def subscribe(self, doc):
        try:
            try:
                first, last = doc['name'].split(' ')[0], doc['name'].split(' ')[1]
            except:
                first, last = doc['name'].split(' ')[0], ''
            m = self.get_mailchimp_api()
            if self.list_id != 'eeea3ac4c6':
                response = m.lists.subscribe(self.list_id, email = {'email':str(doc['email'])}, 
                    double_optin = False,
                    merge_vars = {"FNAME":str(first),"LNAME":str(last),
                    "groupings": [{"name": "Foodtrade Group","groups": [str(doc["sign_up_as"])]}],
                    "mc_location":{"latitude":str(doc["latlng"]["coordinates"][1]),"longitude":str((doc["latlng"]["coordinates"][1]))}},
                    update_existing=True, send_welcome=True, replace_interests=True)
            else:
                response = m.lists.subscribe(self.list_id, email = {'email':str(doc['email'])}, 
                    double_optin = False,
                    merge_vars = {"FNAME":str(first),"LNAME":str(last),
                    "groupings": [{"name": "Foodtrade Group","groups": [str(doc["sign_up_as"])]}],
                    'UserType':str(doc['sign_up_as']),
                    'Name':str(doc['name']),
                    'Postcode':str(doc['zip_code']),
                    "mc_location":{"latitude":str(doc["latlng"]["coordinates"][1]),"longitude":str((doc["latlng"]["coordinates"][1]))}},
                    update_existing=True, send_welcome=True, replace_interests=True)                
            self.save_mailchimp_response({'data_sent':doc, 'response':response})
            return {'status':1}

        except:
            print "Exception on " + doc['email']
            return {'status':0,'message':'Already subscribed'}

class MailChimpException():
    """This class is used to make api calls to the MailChimp"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'mailchimpException'
        self.db_object.create_table(self.table_name,'_id')

    def save_mailchimp_exception(self, doc):
        self.db_object.insert_one(self.table_name, doc)

