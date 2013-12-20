from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.template import RequestContext
from mainapp.TweetFeed import UserProfile
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.models import User

def display_profile(request, username):
    parameters = {}
    user_profile = UserProfile()
    usr = User.objects.get(username = username)
    account = SocialAccount.objects.get(user__id = usr.id)
    userprof = user_profile.get_profile_by_id(str(usr.id))
    parameters['sign_up_as'] = userprof['sign_up_as']
    parameters['address'] = userprof['address']
    parameters['type_user'] = userprof['type_user'].split(',')
    parameters['name'] = account.extra_data['name']
    parameters['description'] = account.extra_data['description']
    parameters['pic_url'] = account.extra_data['profile_image_url']
    print parameters
    if request.user.is_authenticated():
        if parameters['sign_up_as'] == 'Food Business':
            return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))
        elif parameters['sign_up_as'] == 'Organization':
            return render_to_response('single-organization.html', parameters, context_instance=RequestContext(request))
        else:
            return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))           
    else:
        return render_to_response('single-loggedout.php', parameters, context_instance=RequestContext(request))
        