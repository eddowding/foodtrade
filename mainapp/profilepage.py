from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from mainapp.classes.TweetFeed import TweetFeed
from geolocation import get_addr_from_ip
from classes.DataConnector import UserInfo
from mainapp.classes.TweetFeed import Food, TradeConnection, Customer, TradeConnection, UserProfile, Organisation, Team, RecommendFood
from mainapp.classes.Tags import Tags
from mainapp.classes.Foods import AdminFoods
from pygeocoder import Geocoder
import json
from mainapp.produce import *
import random
import time

def resolve_profile(request, username):
    usr = User.objects.get(username = username)
    user_profile = UserProfile()
    userprof = user_profile.get_profile_by_id(str(usr.id))
    if userprof['sign_up_as'] == 'Business':
        return HttpResponseRedirect('/business/'+username)
    elif userprof['sign_up_as'] == 'Individual':
        return HttpResponseRedirect('/person/'+username)
    elif userprof['sign_up_as'] == 'Organisation':
        return HttpResponseRedirect('/organisation/'+username)

def display_profile(request, username):
    parameters = {}
    # parameters['food_list'] = final_foods
    foo = AdminFoods()
    parameters['all_tags'] = foo.get_tags()
    user_profile = UserProfile()
    usr = User.objects.get(username = username)
    account = SocialAccount.objects.get(user__id = usr.id)
    userprof = user_profile.get_profile_by_id(str(usr.id))
    parameters['userprof'] = UserInfo(usr.id)
    parameters['profile_id'] = usr.id
    parameters['sign_up_as'] = userprof['sign_up_as']
    parameters['address'] = userprof['address']
    parameters['type_user'] = userprof['type_user'].split(',')
    parameters['name'] = account.extra_data['name']
    parameters['description'] = account.extra_data['description']
    parameters['pic_url'] = account.extra_data['profile_image_url'].replace("normal","bigger")
    parameters['loc'] = {'lat':userprof['latitude'], 'lon':userprof['longitude']}
    parameters['email'] = usr.email
    parameters['screen_name'] = "@" + account.extra_data['screen_name']

    tweet_feed_obj = TweetFeed()
    updates = tweet_feed_obj.get_tweet_by_user_id(str(usr.id))
    print usr.id, len(updates)
    for i in range(len(updates)):
        time_elapsed = int(time.time()) - updates[i]['time_stamp']
        if time_elapsed<60:
            time_text = str(time_elapsed) + 'seconds'
        elif time_elapsed < 3600:
            minutes = time_elapsed/60
            time_text = str(minutes) + 'minutes'
        elif time_elapsed < 3600*24:
            hours = time_elapsed/3600
            time_text = str(hours) + 'hours'
        elif time_elapsed < 3600*24*365:
            days = time_elapsed/3600/24
            time_text = str(days) + 'days'
        else:
            years = time_elapsed/3600/24/365
            time_text = str(years) + 'years'
        updates[i]['time_elapsed'] = time_text
    parameters['updates'] = updates
    parameters['updates_count'] = len(updates)

    pno = userprof.get('phone_number')
    if pno == None:
        parameters['phone_number'] = ''
    else:
        parameters['phone_number'] = pno
    
    parameters['all_business'] = get_all_business(usr.id)
    if request.user.is_authenticated():
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        parameters['loggedin_signupas'] = user_profile['sign_up_as']
        parameters['loggedin_coord'] = {'lat':user_profile['latitude'], 'lon':user_profile['longitude']}
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        parameters['user_id'] = request.user.id
        lon2 = user_info.lon
        lat2 = user_info.lat

    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]

        else:
            ip = request.META.get('REMOTE_ADDR')
        location_info = get_addr_from_ip(ip)
        lon2 = float(str(location_info['longitude']))
        lat2 = float(str(location_info['latitude']))

    lon2, lat2 = float(str(lon2)), float(str(lat2))
    lon1, lat1 = float(userprof['longitude']),float(userprof['latitude'])
    dis = distance(lon1, lat1, lon2, lat2)
    dis = '%.1f' % (dis * 0.621371)
    parameters['distance'] = dis


        
    if parameters['sign_up_as'] == 'Business':
        if request.user.is_authenticated():
            parameters['connections'], parameters['logged_conn'] = get_connections(usr.id, request.user.id)
            parameters['all_foods'] = get_all_foods(usr.id)
            parameters['organisations'] = get_organisations(usr.id)
            parameters['customers'], parameters['logged_customer'] = get_customers(usr.id, request.user.id)
        else:
            conn_limited, parameters['logged_conn'] = get_connections(usr.id)
            # if not logged in show limited
            parameters['connections'] = conn_limited[:5]
            parameters['all_foods'] = get_all_foods(usr.id)[:3]
            parameters['organisations'] = get_organisations(usr.id)[:3]
            all_customers, parameters['logged_customer'] = get_customers(usr.id)
            parameters['customers'] = all_customers[:10]

        parameters['connections_str'] = json.dumps(parameters['connections'])
        parameters['customers_str'] = json.dumps(parameters['customers'])
        # get all organisations
        return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))
        # return render_to_response('typeahead.html', parameters, context_instance=RequestContext(request))

    elif parameters['sign_up_as'] == 'Organisation':
        parameters['members_foods'], parameters['food_count'] = get_foods_from_org_members(usr.id)
        if request.user.is_authenticated():
            parameters['members'], parameters['logged_member'] = get_members(usr.id, request.user.id)
            parameters['teams'], parameters['logged_team'] = get_team(usr.id, request.user.id)
        else:
            member_limited, parameters['logged_member'] = get_members(usr.id)
            parameters['members'] = member_limited
            team_limited, parameters['logged_team'] = get_team(usr.id)
            parameters['teams'] = team_limited[:10]
        parameters['members_str'] = json.dumps(parameters['members'])
        return render_to_response('single-organization.html', parameters, context_instance=RequestContext(request))
    elif parameters['sign_up_as'] == 'Individual':
        return render_to_response('individual.html', parameters, context_instance=RequestContext(request))
        

def edit_profile(request, username):
    if request.method == 'GET':
        parameters = {}
        tags = Tags()
        parameters['all_tags'] = tags.get_tags()
        if request.user.is_authenticated():
            user_profile = UserProfile()
            account = SocialAccount.objects.get(user__id = request.user.id)
            userprof = user_profile.get_profile_by_id(str(request.user.id))
            parameters['profile_id'] = request.user.id
            parameters['sign_up_as'] = userprof['sign_up_as']
            if userprof['sign_up_as'] == 'Business':
                parameters['type_user'] = str(userprof['type_user'])
            else:
                parameters['type_user'] = ''
            #parameters['zip_code'] = userprof['zip_code']
            parameters['address'] = userprof['address']
            
            try:
                parameters['first_name'] = account.extra_data['name'].split(' ')[0]
                parameters['last_name']  = account.extra_data['name'].split(' ')[1]
            except:
                parameters['first_name']  = account.extra_data['name']
                parameters['last_name']  = ''
            parameters['description'] = account.extra_data['description']
            try:
                parameters['phone'] = userprof['phone_number']
            except:
                parameters['phone'] = ''
            parameters.update(csrf(request))
            user_info = UserInfo(request.user.id)
            parameters['userinfo'] = user_info
            return render_to_response ('editprofile.html', parameters, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/')

    else:
        user_profile = UserProfile()
        userprof = user_profile.get_profile_by_id(str(request.user.id))
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        description = request.POST['description']
        address = request.POST['address']
        try:
            addr_check = Geocoder.geocode(address)
        except:
            address = userprof['address']
        if len(address) == 0:
            address = userprof['address']
        try:
            sign_up_as = request.POST['sign_up_as']
        except:
            userprof = user_profile.get_profile_by_id(str(request.user.id))
            sign_up_as = userprof['sign_up_as']

        phone = request.POST['phone']
        if sign_up_as == 'Business':
            usr_type = request.POST['type']
        else:
            usr_type = ''
        tweetFeedObj = TweetFeed()
        tweetFeedObj.update_tweets(username, first_name, last_name, description, address, sign_up_as, usr_type.split(','))
        user_profile_obj = UserProfile()
        user_profile_obj.update_profile(request.user.id, address, usr_type, sign_up_as, phone)

        usr = User.objects.get(username=username)
        usr.first_name = first_name
        usr.last_name = last_name 
        usr.save()

        twitter_user = SocialAccount.objects.get(user__id = request.user.id)
        twitter_user.extra_data['name'] = first_name + ' ' + last_name
        twitter_user.extra_data['description'] = description
        twitter_user.save()

        return HttpResponseRedirect('/')

def get_all_foods(user_id):
    foo = Food()
    all_foods = foo.get_foods_by_userid(user_id)
    recomm = RecommendFood()
    final_foods = []
    for each in all_foods:
        all_rec = recomm.get_recomm(user_id, each['food_name'])
        recomm_details =  []
        for each_rec in all_rec:
            myid = each_rec['recommenderuid']
            try:
                account = SocialAccount.objects.get(user__id = myid)
                recomm_details.append({'id': myid,
                    'name': account.extra_data['name'],
                    'screen_name': account.extra_data['screen_name'],
                    'photo': account.extra_data['profile_image_url']})
            except:
                pass
        random.shuffle(recomm_details)
        data = {'food_name': each['food_name'], 'vouch_count': len(all_rec), 'recomm_details': recomm_details[:8]}
        final_foods.append(data)
    return final_foods

def get_customers(user_id, logged_id=None):
    cust = Customer()
    all_customers = cust.get_customers_by_userid(user_id)
    final_customers = []
    userprof = UserProfile()
    logged_customer = False
    for each in all_customers:
        account = SocialAccount.objects.get(user__id = each['customeruid'])
        usr_pr = userprof.get_profile_by_id(str(each['customeruid']))
        if logged_id!=None and each['customeruid'] == logged_id:
            logged_customer = True
        final_customers.append({'id': each['customeruid'],
         'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name'],
         'latitude': usr_pr['latitude'],
         'longitude': usr_pr['longitude']
         })
    return final_customers[:10], logged_customer

def get_connections(user_id, logged_in_id = None):
    trade_conn = TradeConnection()
    userprof = UserProfile()
    b_conn = trade_conn.get_connection_by_business(user_id)
    c_conn = trade_conn.get_connection_by_customer(user_id)
    final_connections = []
    logged_conn = 'none'
    for each in b_conn:
        try:
            account = SocialAccount.objects.get(user__id = each['c_useruid'])
            usr_pr = userprof.get_profile_by_id(str(each['c_useruid']))
            user_info = UserInfo(each['c_useruid'])
            if logged_in_id!=None and each['c_useruid'] == logged_in_id:
                logged_conn = 'buyer'
            final_connections.append({'id': each['c_useruid'],
             'name': account.extra_data['name'],
             'description': account.extra_data['description'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'type': usr_pr['type_user'].split(',')[:3],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latitude'],
             'longitude': usr_pr['longitude'],
             'relation': 'buyer'
             })
        except:
            pass
    for each in c_conn:
        try:
            account = SocialAccount.objects.get(user__id = each['b_useruid'])
            usr_pr = userprof.get_profile_by_id(str(each['b_useruid']))
            user_info = UserInfo(each['b_useruid'])
            
            data = {'id': each['b_useruid'],
             'name': account.extra_data['name'],
             'description': account.extra_data['description'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'type': usr_pr['type_user'].split(',')[:3],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latitude'],
             'longitude': usr_pr['longitude'],
             'relation': 'buyer'
             }
            if data not in final_connections:
                data['relation'] = 'seller'
                final_connections.append(data)
                if logged_in_id!=None and each['b_useruid'] == logged_in_id:
                    logged_conn = 'seller'
            else:
                index = final_connections.index(data)
                final_connections[index]['relation'] = 'both'
                if logged_in_id!=None and each['b_useruid'] == logged_in_id:
                    logged_conn = 'both'
        except:
            pass
    return final_connections, logged_conn

def get_members(user_id, logged_in_id = None):
    org = Organisation()
    members = org.get_members_by_orgid(user_id)
    userprof = UserProfile()
    final_members = []
    logged_member = False
    for each in members:
        try:
            account = SocialAccount.objects.get(user__id = each['memberuid'])
            usr_pr = userprof.get_profile_by_id(str(each['memberuid']))
            user_info = UserInfo(each['memberuid'])
            if logged_in_id!=None and each['memberuid'] == logged_in_id:
                    logged_member = True
            final_members.append({'id': each['memberuid'],
             'name': account.extra_data['name'],
             'description': account.extra_data['description'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'type': usr_pr['type_user'].split(','),
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latitude'],
             'longitude': usr_pr['longitude']
             })
        except:
            pass
    return final_members, logged_member

def get_organisations(user_id):
    org = Organisation()
    organisations = org.get_organisations_by_mem_id(user_id)
    final_orgs = []
    for each in organisations:
        account = SocialAccount.objects.get(user__id = each['orguid'])
        final_orgs.append({'id': each['orguid'],
         'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name']
         })
    return final_orgs[:10]

def get_foods_from_org_members(user_id):
    org = Organisation()
    members = org.get_members_by_orgid(user_id)
    foo = Food()
    foods_count = []
    all_foods = []
    for each in members:
        try:
            account = SocialAccount.objects.get(user__id = each['memberuid'])
            mem_foods = foo.get_foods_by_userid(each['memberuid'])
            foods_count.extend(mem_foods)
            all_foods.append({'id': each['memberuid'],
             'name': account.extra_data['name'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'foods': mem_foods
             })
        except:
            pass
    return all_foods, len(foods_count)

def get_team(user_id, logged_in_id=None):
    team = Team()
    teams = team.get_members_by_orgid(user_id)
    final_teams = []
    logged_team = False
    for each in teams:
        try:
            account = SocialAccount.objects.get(user__id = each['memberuid'])
            if logged_in_id!=None and each['memberuid'] == logged_in_id:
                    logged_team = True
            final_teams.append({'id': each['memberuid'],
             'name': account.extra_data['name'],
             'description': account.extra_data['description'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name']
             })
        except:
            pass
    #print final_teams
    return final_teams, logged_team

def get_all_business(prof_id):
    userpro = UserProfile()
    all_business = userpro.get_profile_by_type("Business")
    final_business = []
    for each in all_business:
        try:
            account = SocialAccount.objects.get(user__id = each['useruid'])
            if prof_id != int(each['useruid']):
                final_business.append({'id': each['useruid'],
                    'name': account.extra_data['name'],
                    'description': account.extra_data['description'],
                    'photo': account.extra_data['profile_image_url'],
                    'username' : account.extra_data['screen_name']
                    })
        except:
            pass
    return final_business

from math import radians, cos, sin, asin, sqrt
def distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
