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
from pygeocoder import Geocoder
import json
from mainapp.produce import *

def display_profile(request, username):
    parameters = {}
    parameters['food_list'] = final_foods
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
    parameters['loc'] = {'lat':userprof['latitude'], 'lon':userprof['longitude']}
    parameters['email'] = usr.email
    parameters['screen_name'] = "@" + account.extra_data['screen_name']
    pno = userprof.get('phone_number')
    if pno == 'None':
        parameters['phone_number'] = ''
   
    if request.user.is_authenticated():
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        parameters['user_id'] = request.user.id
        if parameters['sign_up_as'] == 'Business':
            
            parameters['all_foods'] = get_all_foods(usr.id)
            #get all customers
            parameters['customers'] = get_customers(usr.id)
            #get all connections
            parameters['connections'], parameters['logged_conn'] = get_connections(usr.id, request.user.id)
            parameters['connections_str'] = json.dumps(parameters['connections'])
            # get all organisations
            parameters['organisations'] = get_organisations(usr.id)

            return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))
        elif parameters['sign_up_as'] == 'Organisation':
            parameters['members'] = get_members(usr.id)
            parameters['teams'] = get_team(usr.id)
            parameters['members_foods'] = get_foods_from_org_members(usr.id)
            return render_to_response('single-organization.html', parameters, context_instance=RequestContext(request))
        elif parameters['sign_up_as'] == 'Individual':
            return render_to_response('individual.html', parameters, context_instance=RequestContext(request))           
    else:
        return render_to_response('single-loggedout.php', parameters, context_instance=RequestContext(request))
        

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
            parameters['zip_code'] = userprof['zip_code']
            parameters['address'] = userprof['address']
            parameters['type_user'] = str(userprof['type_user'])
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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        description = request.POST['description']
        zip_code = request.POST['zip_code']
        sign_up_as = request.POST['sign_up_as']
        phone = request.POST['phone']

        usr_type = request.POST['type']
        tweetFeedObj = TweetFeed()
        tweetFeedObj.update_tweets(username, first_name, last_name, description, zip_code)
        user_profile_obj = UserProfile()
        user_profile_obj.update_profile(request.user.id, zip_code, usr_type, sign_up_as, phone)

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
        data = {'food_name': each['food_name'], 'vouch_count': len(all_rec)}
        final_foods.append(data)
    return final_foods

def get_customers(user_id):
    cust = Customer()
    all_customers = cust.get_customers_by_userid(user_id)
    final_customers = []
    for each in all_customers:
        account = SocialAccount.objects.get(user__id = each['customeruid'])
        final_customers.append({'id': each['customeruid'],
         'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name']
         })
    return final_customers[:10]

def get_connections(user_id, logged_in_id):
    trade_conn = TradeConnection()
    userprof = UserProfile()
    b_conn = trade_conn.get_connection_by_business(user_id)
    c_conn = trade_conn.get_connection_by_customer(user_id)
    final_connections = []
    logged_conn = 'none'
    for each in b_conn:
        account = SocialAccount.objects.get(user__id = each['c_useruid'])
        usr_pr = userprof.get_profile_by_id(str(each['c_useruid']))
        user_info = UserInfo(each['c_useruid'])
        if each['c_useruid'] == logged_in_id:
            logged_conn = 'buyer'
        final_connections.append({'id': each['c_useruid'],
         'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name'],
         'type': usr_pr['type_user'].split(','),
         'trade_conn_no': user_info.trade_connections_no,
         'food_no': user_info.food_no,
         'org_conn_no': user_info.organisation_connection_no,
         'latitude': usr_pr['latitude'],
         'longitude': usr_pr['longitude'],
         'relation': 'buyer'
         })
    for each in c_conn:
        account = SocialAccount.objects.get(user__id = each['b_useruid'])
        usr_pr = userprof.get_profile_by_id(str(each['b_useruid']))
        user_info = UserInfo(each['b_useruid'])
        if each['b_useruid'] == logged_in_id:
            logged_conn = 'seller'
        data = {'id': each['b_useruid'],
         'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name'],
         'type': usr_pr['type_user'].split(','),
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
        else:
            index = final_connections.index(data)
            final_connections[index]['relation'] = 'both'
    print 'logged_conn', logged_conn
    return final_connections[:10], logged_conn

def get_members(user_id):
    org = Organisation()
    members = org.get_members_by_orgid(user_id)
    userprof = UserProfile()
    final_members = []
    for each in members:
        print each['memberuid']
        account = SocialAccount.objects.get(user__id = each['memberuid'])
        usr_pr = userprof.get_profile_by_id(str(each['memberuid']))
        user_info = UserInfo(each['memberuid'])
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
    return final_members

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
    all_foods = []
    for each in members:
        mem_foods = foo.get_foods_by_userid(each['memberuid'])
        all_foods.extend(mem_foods)
    return all_foods

def get_team(user_id):
    team = Team()
    teams = team.get_members_by_orgid(user_id)
    final_teams = []
    for each in teams:
        account = SocialAccount.objects.get(user__id = each['memberuid'])
        final_teams.append({'id': each['memberuid'],
         'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name']
         })
    #print final_teams
    return final_teams[:10]
