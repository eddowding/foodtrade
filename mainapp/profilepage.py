from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.template import RequestContext
from mainapp.TweetFeed import UserProfile
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from mainapp.TweetFeed import TweetFeed

from geolocation import get_addr_from_ip
from classes.DataConnector import UserInfo

from mainapp.TweetFeed import Food, TradeConnection
from mainapp.classes.Tags import Tags
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
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info

    foo = Food()
    all_foods = foo.get_foods_by_userid(usr.id)
    parameters['all_foods'] = all_foods

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
        

def edit_profile(request, username):
    if request.method == 'GET':
        parameters = {}
        tags = Tags()
        parameters['all_tags'] = tags.get_tags()
        if request.user.is_authenticated():
            user_profile = UserProfile()
            usr = User.objects.get(username = username)
            account = SocialAccount.objects.get(user__id = usr.id)
            userprof = user_profile.get_profile_by_id(str(usr.id))
            parameters['profile_id'] = usr.id
            parameters['sign_up_as'] = userprof['sign_up_as']
            parameters['zip_code'] = userprof['zip_code']
            parameters['address'] = userprof['address']
            parameters['type_user'] = str(userprof['type_user'])
            parameters['first_name'] = usr.first_name
            parameters['last_name']  = usr.last_name
            parameters['description'] = account.extra_data['description']
            parameters.update(csrf(request))
            user_info = UserInfo(usr.id)
            parameters['userinfo'] = user_info
            return render_to_response ('editprofile.html', parameters, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/')

    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        description = request.POST['description']
        zip_code = request.POST['zip_code']
        sign_up_as = request.POST['sign_up_as']

        usr_type = request.POST['type']
        
        tweetFeedObj = TweetFeed()
        tweetFeedObj.update_tweets(username, first_name, last_name, description, zip_code)
        user_profile_obj = UserProfile()
        user_profile_obj.update_profile(request.user.id, zip_code, usr_type, sign_up_as)

        usr = User.objects.get(username=username)
        usr.first_name = first_name
        usr.last_name = last_name 
        usr.save()

        twitter_user = SocialAccount.objects.get(user__id = request.user.id)
        twitter_user.extra_data['name'] = first_name + ' ' + last_name
        twitter_user.extra_data['description'] = description
        twitter_user.save()

        return HttpResponseRedirect('/')












