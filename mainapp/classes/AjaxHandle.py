
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from TweetFeed import TweetFeed
from mainapp.TweetFeed import TradeConnection

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'




class AjaxHandle():
    """docstring for AjaxHandle"""
    def __init__(self):
        pass
    def post_tweet(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        user_id = request.user.id
        st = SocialToken.objects.get(account__user__id=user_id)
        access_token = st.token
        access_token_secret = st.token_secret
        twitter = Twython(
            app_key = consumer_key,
            app_secret = consumer_secret,
            oauth_token = access_token,
            oauth_token_secret = access_token_secret
        )
        # uid = SocialAccount.objects.get(user__id=user_id).uid
        admin_twitter = Twython(
            app_key = consumer_key,
            app_secret = consumer_secret,
            oauth_token = admin_access_token,
            oauth_token_secret = admin_access_token_secret
            )
        message = request.POST.get('message')
        if message != None and message != "":
            twitter.update_status(status = message)
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def add_connection(self, request):
        trade_conn = TradeConnection()
        print request.POST.get('conn_data')
        data = eval(request.POST.get('conn_data'))
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.create_connection({'b_useruid': int(data['prof_id']), 'c_useruid': request.user.id});
            else:
                trade_conn.create_connection({'b_useruid': request.user.id, 'c_useruid': int(data['prof_id'])});
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def del_connection(self, request):
        trade_conn = TradeConnection()
        print request.POST.get('conn_data')
        data = eval(request.POST.get('conn_data'))
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.delete_connection(b_useruid = int(data['prof_id']), c_useruid = request.user.id)
            else:
                trade_conn.delete_connection(b_useruid = request.user.id, c_useruid = int(data['prof_id']))
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")
