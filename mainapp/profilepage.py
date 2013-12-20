from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.template import RequestContext

def display_profile(request, username):
    return render_to_response('singlebusiness.html',context_instance=RequestContext(request))