# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from mainapp.classes.TweetFeed import TweetFeed
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId

from mainapp.classes.Tags import Tags

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'



from classes.DataConnector import UserInfo
from django.template import RequestContext


from mainapp.classes.AjaxHandle import AjaxHandle


from django.views.decorators.csrf import csrf_exempt

def home(request):
    parameters = { }
    return render_to_response('pricing.html',parameters,context_instance=RequestContext(request))

def pages(request, page_name):
    parameters = { }
    return render_to_response(page_name+'.html',parameters,context_instance=RequestContext(request))