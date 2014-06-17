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
from mainapp.single_activity import get_post_parameters
from mainapp.activity import get_search_parameters


from FullSearch import GeneralSearch


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
    def get_latest_updates(self,request):
        search_obj = GeneralSearch(request)
        feed_result = search_obj.get_latest_updates(request.POST.get("time",None))
        return HttpResponse(json.dumps(feed_result))

    def search_profiles(self,request):
        search_obj = GeneralSearch(request)
        profile_result = search_obj.get_result()
        return HttpResponse(json.dumps(profile_result))

    def get_search_result(self,request):
        search_obj = GeneralSearch(request)
        profile_result = search_obj.get_result()
        return HttpResponse(json.dumps(profile_result))

    def single_post_ajax(self,request):
        tweet_id = request.POST.get("parentid",0)
        if tweet_id == 0 :
            return HttpResponse(json.dumps({'status':0}))
        else:
            parameters = get_post_parameters(request,tweet_id)
            ret_val = {}
            ret_val['status'] = 1
            ret_val['result'] = str(render_to_response('single_activity_updates.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
            return HttpResponse(json.dumps(ret_val))
    def ajax_search(self,request):
           
        parameters = get_search_parameters(request)
        ret_val = {}
        ret_val["updates"] = str(render_to_response('activity_updates.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val["indiv"] = str(render_to_response('activity_indiv.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val["biz"] = str(render_to_response('activity_biz.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val["org"] = str(render_to_response('activity_org.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val['results_individual_count'] = parameters['results_individual_count']
        ret_val['results_business_count'] = parameters['results_business_count']
        ret_val['results_organisation_count'] = parameters['results_organisation_count']
        ret_val['results_updates_count'] = parameters['results_updates_count']
        return HttpResponse(json.dumps(ret_val))
