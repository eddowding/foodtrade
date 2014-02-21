from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import Http404
from mainapp.classes.TweetFeed import TweetFeed
from geolocation import get_addr_from_ip
from classes.DataConnector import UserInfo
from mainapp.classes.TweetFeed import Food, TradeConnection, Customer, TradeConnection, UserProfile, Organisation, Team, RecommendFood, ApprovedFoodTags
from mainapp.classes.Tags import Tags
from mainapp.classes.Foods import AdminFoods
from pygeocoder import Geocoder
import json
from mainapp.produce import *
import random
import time
from mainapp.forms import FoodForm
from bson import json_util
from collections import Counter

def resolve_profile(request, username):
    usr_profile = UserProfile()
    userprof = usr_profile.get_profile_by_username(str(username))
    if userprof['sign_up_as'] == 'unclaimed':
        return HttpResponseRedirect('/')
    elif userprof['sign_up_as'] == 'Business':
        return HttpResponseRedirect('/business/'+username)
    elif userprof['sign_up_as'] == 'Individual':
        return HttpResponseRedirect('/person/'+username)
    elif userprof['sign_up_as'] == 'Organisation':
        return HttpResponseRedirect('/organisation/'+username)

def display_profile(request, username):
    if request.method == 'POST':
        food_form = FoodForm(request.POST, request.FILES)
        if food_form.is_valid():
            food_form.save()
        
    parameters = {}
    food_form = FoodForm()
    parameters['form'] = food_form
    foo = AdminFoods()
    parameters['all_tags'] = foo.get_tags()
    usr_profile = UserProfile()
    userprof = usr_profile.get_profile_by_username(str(username))
    uinfo = UserInfo(userprof['useruid'])
    uinfo.description = uinfo.description.replace("\r\n"," ")

    parameters['prof_subscribed'] = uinfo.subscribed
    parameters['userprof'] = uinfo
    parameters['profile_id'] = userprof['useruid']
    parameters['sign_up_as'] = userprof['sign_up_as']
    parameters['address'] = userprof['address']
    parameters['type_user'] = userprof['type_user']
    
    parameters['name'] = userprof.get('business_org_name') if userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation' else userprof['name']

    # parameters['name'] = userprof['name']
    parameters['description'] = userprof['description']
    parameters['pic_url'] = userprof['profile_img'].replace("normal","bigger")

    parameters['loc'] = {'lat':userprof['latlng']['coordinates'][1], 'lon':userprof['latlng']['coordinates'][0]}
    parameters['email'] = userprof['email']
    parameters['screen_name'] = "@" + userprof['screen_name']
    parameters['username'] = userprof['username']
    try:
        parameters['is_unknown_profile'] = userprof['is_unknown_profile']
    except:
        parameters['is_unknown_profile'] = 'false'

    try:
        tweet_feed_obj = TweetFeed()
        user_updates = tweet_feed_obj.get_tweet_by_user_id(userprof['useruid'])
        user_updates["updates"].reverse()
        updates = user_updates["updates"][0:10]

        for i in range(len(updates)):
            time_elapsed = int(time.time()) - updates[i]['time_stamp']
            if time_elapsed<60:
                time_text = str(time_elapsed) + ' seconds'
            elif time_elapsed < 3600:
                minutes = time_elapsed/60
                time_text = str(minutes) + ' minutes'
            elif time_elapsed < 3600*24:
                hours = time_elapsed/3600
                time_text = str(hours) + ' hours'
            elif time_elapsed < 3600*24*365:
                days = time_elapsed/3600/24
                time_text = str(days) + ' days'
            else:
                years = time_elapsed/3600/24/365
                time_text = str(years) + ' years'
            updates[i]['time_elapsed'] = time_text
        parameters['updates'] = updates
        parameters['updates_count'] = len(updates)
    except:
        parameters['updates'] = []
        parameters['updates_count'] = 0

    pno = userprof.get('phone_number')
    if pno == None:
        parameters['phone_number'] = ''
    else:
        parameters['phone_number'] = pno
    
    parameters['all_business'] = get_all_business(userprof['useruid'])
    parameters['all_organisation'] = get_all_orgs(userprof['useruid'])
    if request.user.is_authenticated():
        user_id = request.user.id
        usr_profile_obj = UserProfile()
        usr_profile = usr_profile_obj.get_profile_by_id(str(user_id))
        parameters['loggedin_signupas'] = usr_profile['sign_up_as']
        parameters['loggedin_coord'] = {'lat':usr_profile['latlng']['coordinates'][1], 'lon':usr_profile['latlng']['coordinates'][0]}
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
    lon1, lat1 = float(userprof['latlng']['coordinates'][0]),float(userprof['latlng']['coordinates'][1])
    dis = distance(lon1, lat1, lon2, lat2)
    dis = '%.1f' % (dis * 0.621371)
    parameters['distance'] = dis


        
    if parameters['sign_up_as'] == 'Business':
        if request.user.is_authenticated():
            parameters['connections'], parameters['logged_conn'] = get_connections(userprof['useruid'], request.user.id)
            parameters['all_foods'] = get_all_foods(userprof['useruid'], request.user.id)
            parameters['organisations'] = get_organisations(userprof['useruid'])
            parameters['customers'], parameters['logged_customer'] = get_customers(userprof['useruid'], request.user.id)
        else:
            conn_limited, parameters['logged_conn'] = get_connections(userprof['useruid'])
            # if not logged in show limited
            parameters['connections'] = conn_limited[:5]
            parameters['all_foods'] = get_all_foods(userprof['useruid'])[:3]
            parameters['organisations'] = get_organisations(userprof['useruid'])[:3]
            all_customers, parameters['logged_customer'] = get_customers(userprof['useruid'])
            parameters['customers'] = all_customers[:10]

        parameters['connections_str'] = json.dumps(parameters['connections'])
        parameters['customers_str'] = json.dumps(parameters['customers'])
        # get all organisations
        return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))
        # return render_to_response('typeahead.html', parameters, context_instance=RequestContext(request))

    elif parameters['sign_up_as'] == 'Organisation':
        parameters['members_foods'], parameters['food_count'] = get_foods_from_org_members(userprof['useruid'])
        if request.user.is_authenticated():
            parameters['members'], parameters['logged_member'] = get_members(userprof['useruid'], request.user.id)
            parameters['teams'], parameters['logged_team'] = get_team(userprof['useruid'], request.user.id)
        else:
            member_limited, parameters['logged_member'] = get_members(userprof['useruid'])
            parameters['members'] = member_limited
            team_limited, parameters['logged_team'] = get_team(userprof['useruid'])
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
            usr_profile = UserProfile()
            '''
                If the user is is_authenticated and is super user then he/she can 
                edit all unclaimed accounts.Else he/she can edit only his profile.
            '''
            if request.user.is_superuser:
                userprof = usr_profile.get_profile_by_username(str(username))
                # if userprof.get('is_unknown_profile') == None or userprof.get('is_unknown_profile')=='false':
                #     userprof = usr_profile.get_profile_by_username(str(request.user.username))
            else:
                userprof = usr_profile.get_profile_by_username(str(request.user.username))


            #parameters['profile_id'] = request.user.id
            if request.user.username != username:
                parameters['superuser_edit_other'] = True
            parameters['sign_up_as'] = userprof['sign_up_as']
            parameters['username'] = username
            parameters['company_num'] = userprof.get('company_num') if userprof.get('company_num')!=None else ''
            parameters['website_url'] = userprof.get('website_url') if userprof.get('website_url')!=None else ''
            parameters['facebook_page'] = userprof.get('facebook_page') if userprof.get('facebook_page')!=None else ''
            parameters['deliverables'] = userprof.get('deliverables') if userprof.get('deliverables')!=None else ''
            parameters['business_org_name'] = userprof.get('business_org_name') if userprof.get('business_org_name')!=None else ''

            if userprof['sign_up_as'] == 'Business':
                parameters['type_user'] = str(','.join(userprof['type_user']))
            else:
                parameters['type_user'] = ''
            parameters['address'] = userprof['address']
            parameters['newsletter_freq'] = userprof.get('newsletter_freq') if userprof.get('newsletter_freq')!=None else ''
            parameters['display_name'] = userprof['name']
            parameters['email'] = userprof['email']
            parameters['description'] = userprof['description']
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
        usr_profile = UserProfile()
        '''
            If the user is is_authenticated and is super user then he/she can 
            edit all unclaimed accounts.Else he/she can edit only his profile.       
        '''
        if request.user.is_authenticated:
            if request.user.is_superuser:
                userprof = usr_profile.get_profile_by_username(str(username))
            else:
                userprof = usr_profile.get_profile_by_username(request.user.username)
        else:
            return HttpResponseRedirect('/')

        
        try:
            sign_up_as = request.POST['sign_up_as']
        except:
            sign_up_as = userprof['sign_up_as']
        company_num = request.POST.get('company_num') if request.POST.get('company_num')!=None else ''
        website_url = request.POST.get('website_url') if request.POST.get('website_url')!=None else ''
        facebook_page = request.POST.get('facebook_page') if request.POST.get('facebook_page')!=None else ''
        deliverables = request.POST.get('deliverables') if request.POST.get('deliverables')!=None else ''
        business_org_name = request.POST.get('business_org_name') if request.POST.get('business_org_name')!=None else ''
        print 'business_org_name', business_org_name
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        newsletter_freq = request.POST['newsletter_freq']
        display_name = request.POST['display_name']
        email = request.POST['email']
        # name = first_name + " " + last_name
        description = request.POST['description']
        try:
            lat = request.POST['lat']
            lon = request.POST['lng']
            address = request.POST['formatted_address']
            addr_check = Geocoder.reverse_geocode(float(lat),float(lon))
            postal_code = str(addr_check.postal_code)
            print userprof['latlng']['coordinates'][0]
        except:
            address = userprof['address']
            except_address = Geocoder.geocode(address)
            lat = userprof['latlng']['coordinates'][0]
            lon = userprof['latlng']['coordinates'][1]
            postal_code = userprof['zip_code']

        if len(address) == 0:
            address = userprof['address']

        phone = request.POST['phone']

        if sign_up_as == 'Business':
            usr_type = request.POST['type'].split(",")
        else:
            usr_type = []

        if request.user.is_superuser:
            is_superuser = True
        else:
            is_superuser = False

        usr_profile.update_profile_by_username(userprof['username'], description, address, 
            usr_type, sign_up_as, phone, lat, lon, postal_code, display_name, is_superuser, company_num,
            website_url, facebook_page, deliverables, business_org_name, email, newsletter_freq)

        return HttpResponseRedirect('/')

def get_tags_freq(food_name):
    foo = ApprovedFoodTags()
    foods_list = foo.get_food_by_name(food_name)
    only_tags = foods_list['tags'] if foods_list!=None else ''
    # all_tags = []
    # for eachfoo in foods_list:
    #     if eachfoo.get('approved_food_tags')!= None:
    #         all_tags.extend(eachfoo.get('approved_food_tags').split(','))
    # tags_freq = Counter(all_tags).most_common()
    # only_tags = []
    # for each in tags_freq:
    #     only_tags.append(str(each[0]))
    # only_tags = ','.join(only_tags)
    return only_tags

def get_all_foods(user_id, logged_in_id = None):
    usr_profile = UserProfile()
    
    foo = Food()
    all_foods = foo.get_foods_by_userid(user_id)
    recomm = RecommendFood()
    final_foods = []
    for each in all_foods:
        # get common tags for each foods
        tags_freq = get_tags_freq(each['food_name'])
        all_rec = recomm.get_recomm(user_id, each['food_name'])
        recomm_details =  []
        logged_recommender = False

        for each_rec in all_rec:
            if logged_in_id != None and each_rec['recommenderuid'] == logged_in_id:
                logged_recommender=True
            myid = each_rec['recommenderuid']

            userprof = usr_profile.get_profile_by_id(myid)
            try:
                account = SocialAccount.objects.get(user__id = myid)
                recomm_details.append({'id': myid,
                    'name': userprof.get('business_org_name') if userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation' else userprof['name'],
                    # 'name': account.extra_data['name'],
                    'screen_name': account.extra_data['screen_name'],
                    'photo': account.extra_data['profile_image_url']})
            except:
                pass
        random.shuffle(recomm_details)
        data = {'food_name': each['food_name'], 'vouch_count': len(all_rec), 'recomm_details': recomm_details[:8],
        'logged_recommender': logged_recommender}
        if each.get('description')!=None:
            data['description'] = each.get('description')
        if each.get('food_tags')!=None:
            # tags_list = each.get('food_tags').split(',')
            data['food_tags'] = each.get('food_tags')
        if each.get('photo_url')== None or each.get('photo_url')== '':
            data['photo_url'] = ''
        else:
            data['photo_url'] = each.get('photo_url')
        data['recomm_tags'] = tags_freq
        final_foods.append(data)
    final_foods = sorted(final_foods, key=lambda x: -x['vouch_count'])
    return final_foods

def get_customers(user_id, logged_id=None):
    usr_profile = UserProfile()
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
         'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
         # 'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name'],
         'latitude': usr_pr['latlng']['coordinates'][1],
         'longitude': usr_pr['latlng']['coordinates'][0]
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
             # 'name': account.extra_data['name'],
             'name': usr_pr['business_org_name'] if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
             'description': account.extra_data['description'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'type': usr_pr['type_user'][:3],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latlng']['coordinates'][1],
             'longitude': usr_pr['latlng']['coordinates'][0],
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
             # 'name': account.extra_data['name'],
             'name': userprof.get('business_org_name') if userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation' else userprof['name'],
             'description': account.extra_data['description'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'type': usr_pr['type_user'][:3],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latlng']['coordinates'][1],
             'longitude': usr_pr['latlng']['coordinates'][0],
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
             # 'name': account.extra_data['name'],
             'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
             'description': account.extra_data['description'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'type': usr_pr['type_user'],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latlng']['coordinates'][1],
             'longitude': usr_pr['latlng']['coordinates'][0],
             })
        except:
            pass
    return final_members, logged_member

def get_organisations(user_id):
    userprof = UserProfile()
    org = Organisation()
    organisations = org.get_organisations_by_mem_id(user_id)
    final_orgs = []
    for each in organisations:
        usr_pr = userprof.get_profile_by_id(str(each['orguid']))
        account = SocialAccount.objects.get(user__id = each['orguid'])
        final_orgs.append({'id': each['orguid'],
         # 'name': account.extra_data['name'],
         'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name']
         })
    return final_orgs[:10]

def get_foods_from_org_members(user_id):
    org = Organisation()
    userprof = UserProfile()
    members = org.get_members_by_orgid(user_id)
    foo = Food()
    foods_count = []
    all_foods = []
    for each in members:
        try:
            account = SocialAccount.objects.get(user__id = each['memberuid'])
            usr_pr = userprof.get_profile_by_id(str(each['memberuid']))    
            mem_foods = foo.get_foods_by_userid(each['memberuid'])
            foods_count.extend(mem_foods)
            all_foods.append({'id': each['memberuid'],
             # 'name': account.extra_data['name'],
             'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
             'photo': account.extra_data['profile_image_url'],
             'username' : account.extra_data['screen_name'],
             'foods': mem_foods
             })
        except:
            pass
    return all_foods, len(foods_count)

def get_team(user_id, logged_in_id=None):
    team = Team()
    userprof = UserProfile()
    teams = team.get_members_by_orgid(user_id)
    final_teams = []
    logged_team = False
    for each in teams:
        try:
            usr_pr = userprof.get_profile_by_id(str(each['memberuid']))    
            account = SocialAccount.objects.get(user__id = each['memberuid'])
            if logged_in_id!=None and each['memberuid'] == logged_in_id:
                    logged_team = True
            final_teams.append({'id': each['memberuid'],
             # 'name': account.extra_data['name'],
             'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
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
            print 'all business ', account.extra_data['name']
            usr_pr = userpro.get_profile_by_id(each['useruid'])
            if prof_id != int(each['useruid']):
                final_business.append({'id': each['useruid'],
                    # 'name': account.extra_data['name'],
                    'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
                    'description': account.extra_data['description'],
                    'photo': account.extra_data['profile_image_url'],
                    'username' : account.extra_data['screen_name']
                    })
        except:
            pass
    print 'final_business', final_business
    return final_business

def get_all_orgs(prof_id):
    userpro = UserProfile()
    all_organisation = userpro.get_profile_by_type("Organisation")
    final_organisation = []
    for each in all_organisation:
        try:
            account = SocialAccount.objects.get(user__id = each['useruid'])
            usr_pr = userprof.get_profile_by_id(str(each['useruiduid']))    
            if prof_id != int(each['useruid']):
                final_organisation.append({'id': each['useruid'],
                    # 'name': account.extra_data['name'],
                    'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
                    'description': account.extra_data['description'],
                    'photo': account.extra_data['profile_image_url'],
                    'username' : account.extra_data['screen_name']
                    })
        except:
            pass
    return final_organisation    

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
