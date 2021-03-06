#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from mainapp.classes.TweetFeed import TweetFeed, UserProfile, Friends, TwitterError, Invites, InviteId, Notification, Analytics
from django.template import RequestContext
import datetime
import time
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from twython import Twython
from mainapp.views import get_twitter_obj
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

@csrf_exempt
def update_image(request):
    img_url = request.POST.get('img')
    img_url = img_url.replace("bigger","normal")
    img_url = img_url.replace("/web_retina","")
    up = UserProfile()
    try:
        user_details = up.get_profile_by_profile_img(img_url)
        bot_twitter = get_twitter_obj(settings.BOT_ACCESS_TOKEN, settings.BOT_ACCESS_TOKEN_SECRET)
        details = bot_twitter.show_user(screen_name=user_details['username'])
        image_desc = {'profile_img': details['profile_image_url']}
        up.update_profile_fields({"useruid":user_details['useruid']}, image_desc)
        return HttpResponse(json.dumps({"status":"ok","src":details['profile_image_url']}))

    except:
        try:
            user_details = up.get_profile_by_profile_banner_url(img_url)
            bot_twitter = get_twitter_obj(settings.BOT_ACCESS_TOKEN, settings.BOT_ACCESS_TOKEN_SECRET)
            details = bot_twitter.show_user(screen_name=user_details['username'])       
            image_desc = {'profile_banner_url': details.get("profile_background_image_url_https","")}


            up.update_profile_fields({"useruid":user_details['useruid']}, image_desc)
            return HttpResponse(json.dumps({"status":"ok","src":details.get("profile_background_image_url_https","")}))
        except:
            pass

    return HttpResponse(json.dumps({"status":"error","message":"No image was found"}))