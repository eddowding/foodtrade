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
consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'


class AjaxFunc():
    """docstring for AjaxHandle"""
    def __init__(self):
        pass
    
    def delete_tweet(self,request):
        tweet_id= int(request.POST.get('id'))
        tweet = TweetFeed()
        tweet.delete_tweet(tweet_id)
        
