#!/usr/bin/env python
# encoding: utf-8
from MongoConnection import MongoConnection
from bson.objectid import ObjectId
from pygeocoder import Geocoder
from bson.code import Code
from bson import BSON
from bson import json_util
from pymongo import Connection
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from twython import Twython
import json, time, datetime


class ProfileVisits():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'profilevisits'

    def save_visit(self,data={}):
    	return self.db_object.insert_one(self.table_name, data)

    def get_visit_stats(self, pagenum=1, conditions={}):
    	return self.db_object.get_paginated_values(self.table_name, conditions=conditions, pageNumber=pagenum)

    


    