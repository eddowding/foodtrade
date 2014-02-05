# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from mainapp.geolocation import get_addr_from_ip
from mainapp.classes.TweetFeed import TweetFeed
from mainapp.classes.Email import Email
from Tags import Tags
from mainapp.classes.TweetFeed import TradeConnection, UserProfile, Food, Customer, Organisation, Team, RecommendFood
from Search import Search
import time
from mainapp.classes.DataConnector import UserInfo

from mainapp.activity import get_search_parameters
consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'




class AjaxSearch():
    """docstring for AjaxHandle"""
    def __init__(self):
        pass
    
    def ajax_search(self,request):
           
        parameters = get_search_parameters(request)
        ret_val = {}
        ret_val["updates"] = str(render_to_response('activity_updates.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val["biz"] = str(render_to_response('activity_biz.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val["org"] = str(render_to_response('activity_org.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val['results_business_count'] = parameters['results_business_count']
        ret_val['results_organisation_count'] = parameters['results_organisation_count']
        ret_val['results_updates_count'] = parameters['results_updates_count']
        return HttpResponse(json.dumps(ret_val))
