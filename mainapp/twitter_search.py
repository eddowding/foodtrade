from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import Http404
from mainapp.classes.TweetFeed import TweetFeed
from geolocation import get_addr_from_ip
from classes.DataConnector import UserInfo
from mainapp.classes.TweetFeed import Food, TradeConnection, Customer, TradeConnection, UserProfile, Organisation, Team, RecommendFood, ApprovedFoodTags
from mainapp.classes.Tags import Tags
from mainapp.classes.Foods import AdminFoods
from pygeocoder import Geocoder
import json
from mainapp.produce import *
import random
import time
from mainapp.forms import FoodForm
from bson import json_util
from collections import Counter
import pprint
from django.http import Http404



def search_users(request):
    if request.user.is_authenticated():
    	query = request.GET.get("q")

        user_id = request.user.id
        tweet_feed_obj = TweetFeed()
        results = tweet_feed_obj.search_tweeter_users(user_id, query)
        return HttpResponse(json.dumps(results))
    else:
        return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized to perform this action.'}))        

