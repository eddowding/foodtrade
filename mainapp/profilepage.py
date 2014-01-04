from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.template import RequestContext
from mainapp.TweetFeed import UserProfile
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.models import User

from geolocation import get_addr_from_ip
from classes.DataConnector import UserInfo
def display_profile(request, username):
    parameters = {}
    user_profile = UserProfile()
    usr = User.objects.get(username = username)
    account = SocialAccount.objects.get(user__id = usr.id)
    userprof = user_profile.get_profile_by_id(str(usr.id))
    parameters['profile_id'] = usr.id
    parameters['sign_up_as'] = userprof['sign_up_as']
    parameters['address'] = userprof['address']
    parameters['type_user'] = userprof['type_user'].split(',')
    parameters['name'] = account.extra_data['name']
    parameters['description'] = account.extra_data['description']
    parameters['pic_url'] = account.extra_data['profile_image_url']

    if request.user.is_authenticated():
        # parameters['user'] = request.user
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))

        # default_lon = float(user_profile['longitude'])
        # default_lat = float(user_profile['latitude'])
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info



    # else:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    location_info = get_addr_from_ip(ip)
    default_lon = float(location_info['longitude'])
    default_lat = float(location_info['latitude'])

    parameters['loc'] = {'lat':default_lat, 'lon':default_lon}
    if request.user.is_authenticated():
        if parameters['sign_up_as'] == 'Food Business':
            return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))
        elif parameters['sign_up_as'] == 'Organization':
            return render_to_response('single-organization.html', parameters, context_instance=RequestContext(request))
        else:
            return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))           
    else:
        return render_to_response('single-loggedout.php', parameters, context_instance=RequestContext(request))
        