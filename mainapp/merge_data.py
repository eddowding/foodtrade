#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from django.conf import settings
from mainapp.classes.Email import Email
from mainapp.classes.TweetFeed import TweetFeed, UserProfile, Friends, TwitterError, Invites, InviteId, Notification, Analytics
from mainapp.classes.mailchimp import MailChimp, MailChimpException
from mainapp.classes.Tags import Tags
from search import *
from streaming import MyStreamer
from models import MaxTweetId
from geolocation import get_addr_from_ip
from django.template import RequestContext
import datetime
from django.core.context_processors import csrf
import time
from pygeocoder import Geocoder
from mainapp.classes.DataConnector import UserInfo
import pprint
from django.contrib.auth.models import User
from mainapp.bitly import construct_invite_tweet
from django.contrib.auth.decorators import user_passes_test
import HTMLParser
from mainapp.classes.Search import Search
from mainapp.classes.Email import Email
import uuid
from twilio.rest import TwilioRestClient 
from mainapp.classes.mailchimp import MailChimp
from mainapp.classes.SendSms import send_sms


def merge(request):
    token = request.GET.get("token")
    if token == "update":
        tweet_feed = TweetFeed()
        business_users = tweet_feed.get_all_users()
        for user in business_users:
            twt = TweetFeed()
            twt.update_data(user)
        return HttpResponse("success"+json.dumps(business_users))
    return HttpResponse("sorry")