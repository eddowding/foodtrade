#!/usr/bin/env python
# encoding: utf-8
from MongoConnection import MongoConnection
from bson.objectid import ObjectId

class TwitterError():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'twittererror'
        self.db_object.create_table(self.table_name,'screen_name')    

    def save_error(self, doc):
        return self.db_object.update_upsert(self.table_name,{'username':doc['username']}, doc)

    def get_error(self, screen_name, error_type=''):
        if error_type=='':
            return self.db_object.get_all_vals(self.table_name,{'screen_name':screen_name, 'error_solve_stat':'false','error_type':{'$exists':False}})   
        elif error_type=='cron':
            return self.db_object.get_all_vals(self.table_name,{'screen_name':screen_name, 'error_solve_stat':'false', 'error_type':'cron'})

    def change_error_status(self, screen_name, error_type=''):
        if error_type=='':
            return self.db_object.update(self.table_name, {'screen_name':screen_name,'error_type':{'$exists':False}}, {'error_solve_stat':'true'})
        else:
            return self.db_object.update(self.table_name, {'screen_name':screen_name,'error_type':'cron'},{'error_solve_stat':'true'})

    def get_unsolved_error(self, error_type):
        if error_type=='cron':
            errors = []            
            errors_pages_count = int(self.db_object.get_count(self.table_name, {'error_solve_stat':'false','error_type':{'$exists':False}})/15)+ 1            
            for i in range(0,errors_pages_count, 1):
                pag_errors = self.db_object.get_paginated_values(self.table_name, {'error_solve_stat':'false','error_type':{'$exists':False}}, pageNumber = int(i+1))
                for eachError in pag_errors:
                    errors.append(eachError)
            return users