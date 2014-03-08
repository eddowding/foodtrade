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
            if int(user) > 1:

                up = UserProfile()
                user_details = up.get_profile_by_id(user)
                st = SocialToken.objects.get(account__user__id=user)
                ACCESS_TOKEN = st.token
                ACCESS_TOKEN_SECRET = st.token_secret
                user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
                details = user_twitter.show_user(screen_name=user_details['username'])
                image_desc = {'profile_img': details['profile_image_url']}
                up.update_profile_fields({"useruid":user}, image_desc)

        return HttpResponse("success"+json.dumps(business_users))

    return HttpResponse("sorry")

@csrf_exempt
def update_image(request):
    img_url = request.POST.get('img')



    up = UserProfile()
    user_details = up.get_profile_by_profile_img(img_url)
    st = SocialToken.objects.get(account__user__id=user)
    ACCESS_TOKEN = st.token
    ACCESS_TOKEN_SECRET = st.token_secret
    user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    details = user_twitter.show_user(screen_name=user_details['username'])
    image_desc = {'profile_img': details['profile_image_url']}
    up.update_profile_fields({"useruid":user_details['useruid']}, image_desc)
    return HttpResponse("sorry")
