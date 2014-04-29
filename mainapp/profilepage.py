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
import pprint
from django.http import Http404
import re
from mainapp.classes.MongoConnection import MongoConnection
from embedly import Embedly
from django.conf import settings
from mainapp.classes.TwitterCounts import TwitterCounts
from mainapp.classes.TweetFeed import Friends



def profile_url_resolve(request, username):
    if username == 'me':
        if request.user.is_authenticated():
            username = request.user.username
        else:
            return HttpResponseRedirect('/accounts/twitter/login/?process=login')            
    usr_profile = UserProfile()
    userprof = usr_profile.get_profile_by_username(str(username))

    if userprof!= None:
        return display_profile(request, userprof['username'])
    else:
        try:
            from mainapp.classes.AjaxHandle import AjaxHandle
            user_id = request.user.id
            tweet_feed_obj = TweetFeed()
            result = tweet_feed_obj.search_tweeter_users(user_id, username, 1)
            ajax_handle = AjaxHandle()
            ajax_handle.create_fake_profile(result[0]['screen_name'], result[0]['screen_name'], 'twitter','unclaimed')
            userprof = usr_profile.get_profile_by_username(str(result[0]['screen_name']))            
            return HttpResponseRedirect('/' + str(result[0]['screen_name']))
        except:
            raise Http404
            
def resolve_profile(request, username):
    if username == 'me':
        if request.user.is_authenticated():
            username = request.user.username
            return display_profile(request, username)    
    usr_profile = UserProfile()
    
    userprof = usr_profile.get_profile_by_username(str(username))
    if userprof == None:
        try:
            from mainapp.classes.AjaxHandle import AjaxHandle
            user_id = request.user.id
            tweet_feed_obj = TweetFeed()
            result = tweet_feed_obj.search_tweeter_users(user_id, username, 1)
            ajax_handle = AjaxHandle()
            ajax_handle.create_fake_profile(result[0]['screen_name'], result[0]['screen_name'], 'twitter','unclaimed')
            userprof = usr_profile.get_profile_by_username(str(result[0]['screen_name']))            
            return HttpResponseRedirect('/profile/' + str(result[0]['screen_name']))
        except:
            raise Http404

    if userprof['sign_up_as'] == 'unclaimed':
        return HttpResponseRedirect('/unclaimed/' + username)
    elif userprof['sign_up_as'] == 'Business':
        return HttpResponseRedirect('/business/'+username)
    elif userprof['sign_up_as'] == 'Individual':
        return HttpResponseRedirect('/person/'+username)
    elif userprof['sign_up_as'] == 'Organisation':
        return HttpResponseRedirect('/organisation/'+username)

def display_profile(request, username):
    if request.method == 'POST':
        month_list = []
        for i in range(1,13):
            val = request.POST.get('option'+str(i)+'_month')
            month_list.append(1) if val=='on' else month_list.append(0)
        food_form = FoodForm(request.POST, request.FILES)
        if food_form.is_valid():
            food_form.save(month_list)
        
    parameters = {}
    
    twitter_counts = TwitterCounts()
    f_count = twitter_counts.get_twitter_followers_and_number(request.user.id, username)    
    parameters['followers_count'] = f_count['followers_count']
    parameters['friends_count'] = f_count['friends_count']
    parameters['banner_url'] = f_count['banner_url']

    food_form = FoodForm()
    parameters['form'] = food_form
    foo = AdminFoods()

    parameters['all_tags'] = foo.get_tags()

    user_profile = UserProfile()
    try:
        userprof = user_profile.get_profile_by_username(str(username))
        a = userprof['sign_up_as']
    except:
        raise Http404
    uinfo = UserInfo(userprof['useruid'])
    uinfo.description = uinfo.description.replace("\r\n"," ")

    parameters['prof_subscribed'] = uinfo.subscribed
    parameters['userprof'] = uinfo
    try:
        parameters['show_foods'] = userprof['show_foods']
    except:
        parameters['show_foods'] = True


    rec_food_obj = RecommendFood()
    parameters['total_vouches'] =rec_food_obj.get_recommend_count(userprof['useruid'])

    parameters['profile_id'] = userprof['useruid']
    parameters['sign_up_as'] = userprof['sign_up_as']
    parameters['address'] = userprof['address']
    parameters['type_user'] = userprof['type_user']

    video_url = userprof.get('video_url') if userprof.get('video_url')!=None else ''
    if video_url != '':
        parameters['intro_video'] = get_video_html(video_url)
    else:
        parameters['intro_video'] = ''
    try:
        parameters['company_num'] = userprof.get('company_num') if userprof.get('company_num')!=None else ''
        parameters['website_url'] = userprof.get('website_url') if userprof.get('website_url')!=None else ''
        parameters['facebook_page'] = userprof.get('facebook_page') if userprof.get('facebook_page')!=None else ''
        parameters['deliverables'] = userprof.get('deliverables') if userprof.get('deliverables')!=None else ''
        parameters['business_org_name'] = userprof.get('business_org_name') if userprof.get('business_org_name')!=None else ''    
    except:
        pass
    
    parameters['we_buy'] = userprof.get('we_buy') if userprof.get('we_buy')!=None else ''

    if userprof.get('business_org_name')!=None:
        parameters['name'] = userprof.get('business_org_name') if (userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation') \
        and userprof.get('business_org_name')!='' else userprof['name']
    else:
        parameters['name'] = userprof['name']
    
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
        updates = user_updates["updates"]
        new_updates = []

        '''Show only undeleted posts'''
        for eachUpdate in updates:
            if eachUpdate['deleted'] == 0:
                new_updates.append(eachUpdate)
        updates = new_updates[0:10]

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
    
    # parameters['all_business'] = get_all_business(userprof['useruid'])
    # parameters['all_organisation'] = get_all_orgs()
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
            parameters['all_buying_foods'] = get_all_buying_foods(userprof['useruid'], request.user.id)
            
            parameters['organisations'] = get_organisations(userprof['useruid'])
            parameters['customers'], parameters['logged_customer'] = get_customers(userprof['useruid'], request.user.id)
        else:
            conn_limited, parameters['logged_conn'] = get_connections(userprof['useruid'])

            # if not logged in show limited
            parameters['connections'] = conn_limited
            parameters['all_foods'] = get_all_foods(userprof['useruid'])[:3]
            parameters['organisations'] = get_organisations(userprof['useruid'])[:3]
            all_customers, parameters['logged_customer'] = get_customers(userprof['useruid'])
            parameters['customers'] = all_customers[:10]

        parameters['connections_str'] = json.dumps(parameters['connections'])
        parameters['customers_str'] = json.dumps(parameters['customers'])
        return render_to_response('singlebusiness.html', parameters, context_instance=RequestContext(request))

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
        if request.user.is_authenticated():
            parameters['all_foods'] = get_all_foods(userprof['useruid'], request.user.id)
        else:
            parameters['all_foods'] = get_all_foods(userprof['useruid'])[:3]
        return render_to_response('individual.html', parameters, context_instance=RequestContext(request))
        
    elif parameters['sign_up_as']=='unclaimed':
        return render_to_response('single-unknown.html', parameters, context_instance=RequestContext(request))
        

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
                try:
                    if username == 'me':
                       userprof = usr_profile.get_profile_by_username(str(request.user.username))
                    else:
                        userprof = usr_profile.get_profile_by_username(str(username))
                    a = userprof['sign_up_as']
                except:
                    raise Http404
                # if userprof.get('is_unknown_profile') == None or userprof.get('is_unknown_profile')=='false':
                #     userprof = usr_profile.get_profile_by_username(str(request.user.username))
            else:
                userprof = usr_profile.get_profile_by_username(str(request.user.username))


            #parameters['profile_id'] = request.user.id
            if request.user.username != username:
                parameters['superuser_edit_other'] = True
            parameters['sign_up_as'] = userprof['sign_up_as']
            parameters['username'] = username
            parameters['video_url'] = userprof.get('video_url') if userprof.get('video_url')!=None else ''
            parameters['we_buy'] = userprof.get('we_buy') if userprof.get('we_buy')!=None else ''

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
            try:
                parameters['show_foods'] = userprof['show_foods']
            except:
                parameters['show_foods'] = True
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
        if request.user.is_authenticated():
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
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        newsletter_freq = request.POST['newsletter_freq']
        display_name = request.POST['display_name']
        video_url = request.POST.get('video_url')
        we_buy = request.POST.get('we_buy')
        email = request.POST['email']
        # name = first_name + " " + last_name
        description = request.POST['description']
        try:
            lat = request.POST['lat']
            lon = request.POST['lng']
            address = request.POST['formatted_address']
            addr_check = Geocoder.reverse_geocode(float(lat),float(lon))
            postal_code = str(addr_check.postal_code)
        except:
            address = userprof['address']
            lat = userprof['latlng']['coordinates'][1]
            lon = userprof['latlng']['coordinates'][0]
            postal_code = userprof['zip_code']

        if len(address) == 0:
            address = userprof['address']

        phone = request.POST['phone']

        if sign_up_as == 'Business':
            usr_type = request.POST['type'].split(",")
        else:
            usr_type = []
        try:
            show_foods = request.POST['show_foods']
        except:
            show_foods = 'Yes'
        show_food_db = True if show_foods == 'Yes' else False

        if request.user.is_superuser:
            is_superuser = True
        else:
            is_superuser = False

        usr_profile.update_profile_by_username(userprof['username'], description, address, 
            usr_type, sign_up_as, phone, lat, lon, postal_code, display_name, is_superuser, company_num,
            website_url, facebook_page, deliverables, business_org_name, email, newsletter_freq, show_food_db, video_url)
        twt = TweetFeed()
        twt.update_data(userprof['useruid'])

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
    # find out hierarchy
    adm = AdminFoods()
    adm_foods = adm.get_tags()


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
                # account = SocialAccount.objects.get(user__id = myid)
                if userprof.get('business_org_name')!=None:
                    myname = userprof.get('business_org_name') if (userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation') \
                    and userprof.get('business_org_name')!='' else userprof['name']
                else:
                    myname = userprof['name']                
                recomm_details.append({'id': myid,
                    'name': myname,
                    # 'name': userprof.get('business_org_name') if userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation' else userprof['name'],
                    # 'name': account.extra_data['name'],
                    'screen_name': userprof['screen_name'],
                    'photo': userprof['profile_img']})
            except:
                pass
        random.shuffle(recomm_details)
        data = {'food_name': each['food_name'], 'vouch_count': len(all_rec), 'recomm_details': recomm_details[:8],
        'logged_recommender': logged_recommender}
        if each.get('description')!=None:
            data['description'] = each.get('description')

        data['how_much'] = each.get('how_much') if each.get('how_much')!=None else ''
        data['how_often'] = each.get('how_often') if each.get('how_often')!=None else 'How often'
        data['month_list'] = each.get('month_list') if each.get('month_list')!=None else []


        if each.get('food_tags')!=None:
            # tags_list = each.get('food_tags').split(',')
            data['food_tags'] = each.get('food_tags')
        if each.get('photo_url')== None or each.get('photo_url')== '':
            data['photo_url'] = ''
        else:
            data['photo_url'] = each.get('photo_url')
        data['recomm_tags'] = tags_freq

        #find and append food hierarchy
        for each_adm in adm_foods:
            if each_adm.get('childrens')!=None:
                foo_list = [x['node'] for x in each_adm['childrens']]
                if each['food_name'] in foo_list:
                    data['parent_food'] = each_adm['node']
                    break
        final_foods.append(data)
    final_foods = sorted(final_foods, key=lambda x: -x['vouch_count'])
    return final_foods

def get_all_buying_foods(user_id, logged_in_id = None):
    usr_profile = UserProfile()
    # find out hierarchy
    adm = AdminFoods()
    adm_foods = adm.get_tags()

    foo = Food()
    all_foods = foo.get_webuy_foods_by_userid(user_id)
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
                # account = SocialAccount.objects.get(user__id = myid)
                if userprof.get('business_org_name')!=None:
                    myname = userprof.get('business_org_name') if (userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation') \
                    and userprof.get('business_org_name')!='' else userprof['name']
                else:
                    myname = userprof['name']                
                recomm_details.append({'id': myid,
                    'name': myname,
                    # 'name': userprof.get('business_org_name') if userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation' else userprof['name'],
                    # 'name': account.extra_data['name'],
                    'screen_name': userprof['screen_name'],
                    'photo': userprof['profile_img']})
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

        #find and append food hierarchy
        for each_adm in adm_foods:
            if each_adm.get('childrens')!=None:
                foo_list = [x['node'] for x in each_adm['childrens']]
                if each['food_name'] in foo_list:
                    data['parent_food'] = each_adm['node']
                    break
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
        # account = SocialAccount.objects.get(user__id = each['customeruid'])
        usr_pr = userprof.get_profile_by_id(str(each['customeruid']))
        if logged_id!=None and each['customeruid'] == logged_id:
            logged_customer = True
        if usr_pr.get('business_org_name')!=None:
            myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
            and usr_pr.get('business_org_name')!='' else usr_pr['name']
        else:
            myname = usr_pr['name']                        
        final_customers.append({'id': each['customeruid'],
        'name': myname,
         # 'name': usr_pr.get('business_org_name') if usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation' else usr_pr['name'],
         # 'name': account.extra_data['name'],
         'description': usr_pr['description'],
         'photo': usr_pr['profile_img'],
         'username' : usr_pr['username'],
         'latitude': usr_pr['latlng']['coordinates'][1],
         'longitude': usr_pr['latlng']['coordinates'][0],
         'banner_url': get_banner_url(useruid = int(each['customeruid']))
         })
    return final_customers[:10], logged_customer

def get_connections(user_id, logged_in_id = None):
    trade_conn = TradeConnection()
    userprof = UserProfile()
    b_conn = trade_conn.get_connection_by_business(user_id)
    c_conn = trade_conn.get_connection_by_customer(user_id)
    final_connections = []
    print 'b_conn: ', len(b_conn), 'c_conn: ', len(c_conn)
    logged_conn = 'none'
    for count, each in enumerate(b_conn):
        try:
            if logged_in_id == None and count == 5:
                break
            # account = SocialAccount.objects.get(user__id = each['c_useruid'])
            
            usr_pr = userprof.get_profile_by_id(str(each['c_useruid']))
            user_info = UserInfo(each['c_useruid'])
            if logged_in_id!=None and each['c_useruid'] == logged_in_id:
                logged_conn = 'buyer'
            if usr_pr.get('business_org_name')!=None:
                myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
                and usr_pr.get('business_org_name')!='' else usr_pr['name']
            else:
                myname = usr_pr['name']                            
            final_connections.append({'id': each['c_useruid'],
             # 'name': account.extra_data['name'],
             'name': myname,
             'description': usr_pr['description'],
             'photo': usr_pr['profile_img'],
             'username' : usr_pr['username'],
             'type': usr_pr['type_user'][:3],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latlng']['coordinates'][1],
             'longitude': usr_pr['latlng']['coordinates'][0],
             'relation': 'buyer',
             'banner_url': get_banner_url(useruid = int(each['c_useruid']), logged_useruid=logged_in_id)
             })
            
        except:
            pass
    for count, each in enumerate(c_conn):
        try:
            if logged_in_id == None and count == 5:
                break

            usr_pr = userprof.get_profile_by_id(str(each['b_useruid']))
            user_info = UserInfo(each['b_useruid'])
            if usr_pr.get('business_org_name')!=None:
                myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
                and usr_pr.get('business_org_name')!='' else usr_pr['name']
            else:
                myname = usr_pr['name']                                        
            data = {'id': each['b_useruid'],
             # 'name': account.extra_data['name'],
             'name': myname,
             'description': usr_pr['description'],
             'photo': usr_pr['profile_img'],
             'username' : usr_pr['username'],
             'type': usr_pr['type_user'][:3],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latlng']['coordinates'][1],
             'longitude': usr_pr['latlng']['coordinates'][0],
             'relation': 'buyer',
             'banner_url': get_banner_url(useruid = int(each['b_useruid']), logged_useruid=logged_in_id)
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
            # account = SocialAccount.objects.get(user__id = each['memberuid'])
            usr_pr = userprof.get_profile_by_id(str(each['memberuid']))
            user_info = UserInfo(each['memberuid'])
            if logged_in_id!=None and each['memberuid'] == logged_in_id:
                    logged_member = True
            if usr_pr.get('business_org_name')!=None:
                myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
                and usr_pr.get('business_org_name')!='' else usr_pr['name']
            else:
                myname = usr_pr['name']                    
            final_members.append({'id': each['memberuid'],
             # 'name': account.extra_data['name'],
             'name': myname,
             'description': usr_pr['description'],
             'photo': usr_pr['profile_img'],
             'username' : usr_pr['username'],
             'type': usr_pr['type_user'],
             'trade_conn_no': user_info.trade_connections_no,
             'food_no': user_info.food_no,
             'org_conn_no': user_info.organisation_connection_no,
             'latitude': usr_pr['latlng']['coordinates'][1],
             'longitude': usr_pr['latlng']['coordinates'][0],
             'banner_url': get_banner_url(useruid = int(each['memberuid']), logged_useruid= logged_in_id)
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
        # account = SocialAccount.objects.get(user__id = each['orguid'])
        if usr_pr.get('business_org_name')!=None:
            myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
            and usr_pr.get('business_org_name')!='' else usr_pr['name']
        else:
            myname = usr_pr['name']                                    
        final_orgs.append({'id': each['orguid'],
         # 'name': account.extra_data['name'],
         'name': myname,
         'description': usr_pr['description'],
         'photo': usr_pr['profile_img'],
         'username' : usr_pr['username'],
         'banner_url': get_banner_url(useruid = int(each['orguid']))
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
            # account = SocialAccount.objects.get(user__id = each['memberuid'])
            usr_pr = userprof.get_profile_by_id(str(each['memberuid']))    
            mem_foods = foo.get_foods_by_userid(each['memberuid'])
            foods_count.extend(mem_foods)
            if usr_pr.get('business_org_name')!=None:
                myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
                and usr_pr.get('business_org_name')!='' else usr_pr['name']
            else:
                myname = usr_pr['name']                                        
            all_foods.append({'id': each['memberuid'],
             # 'name': account.extra_data['name'],
             'name': myname,
             'photo': usr_pr['profile_img'],
             'username' : usr_pr['username'],
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
            # account = SocialAccount.objects.get(user__id = each['memberuid'])
            if logged_in_id!=None and each['memberuid'] == logged_in_id:
                    logged_team = True
            if usr_pr.get('business_org_name')!=None:
                myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
                and usr_pr.get('business_org_name')!='' else usr_pr['name']
            else:
                myname = usr_pr['name']                            
            final_teams.append({'id': each['memberuid'],
             # 'name': account.extra_data['name'],
             'name': myname,
             'description': usr_pr['description'],
             'photo': usr_pr['profile_img'],
             'username' : usr_pr['username'],
             'banner_url': get_banner_url(useruid = int(each['memberuid']), logged_useruid=logged_in_id)
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
            # account = SocialAccount.objects.get(user__id = each['useruid'])
            usr_pr = userpro.get_profile_by_id(each['useruid'])
            if usr_pr.get('business_org_name')!=None:
                myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
                and usr_pr.get('business_org_name')!='' else usr_pr['name']
            else:
                myname = usr_pr['name']                                        
            if prof_id != int(each['useruid']):
                final_business.append({'id': each['useruid'],
                    # 'name': account.extra_data['name'],
                    'name': myname,
                     'description': usr_pr['description'],
                     'photo': usr_pr['profile_img'],
                     'username' : usr_pr['username']
                    })
        except:
            pass
    return final_business

def get_all_orgs():
    userpro = UserProfile()
    all_organisation = userpro.get_profile_by_type("Organisation")
    final_organisation = []
    for each in all_organisation:
        
        if each.get('business_org_name')!=None:
            myname = each.get('business_org_name') if (each['sign_up_as'] == 'Business' or each['sign_up_as'] == 'Organisation') \
            and each.get('business_org_name')!='' else each['name']
        else:
            myname = each['name']                                            
        final_organisation.append({'id': each['useruid'],
            'name':myname
            })

    return final_organisation    

def search_orgs_business(request, type_user):
    if request.user.is_authenticated():
        query = request.GET.get("q")
        user_id = request.user.id

        referal_url = request.META.get('HTTP_REFERER')
        split_user = referal_url.split('/')
        profile_user = split_user[-2] if split_user[-2] != 'me' else request.user.username

        userpro = UserProfile()
        profile_user_obj = userpro.get_profile_by_username(profile_user)
        if type_user == 'Business':
            type_user_new = [type_user]
            profile_data = get_connections(profile_user_obj['useruid'], request.user.id)[0]
        elif type_user == 'Organisation':
            type_user_new = [type_user]
            profile_data = get_organisations(profile_user_obj['useruid'])
        elif type_user == 'Member':
            type_user_new = ['Business', 'Organisation', 'Individual']
            profile_data = get_members(profile_user_obj['useruid'], request.user.id)[0]

        data_list = [int(each['id']) for each in profile_data]
        keyword_like = re.compile(query + '+', re.IGNORECASE)
        reg_expression = {"$regex": keyword_like, '$options': '-i'}

        search_variables = ["name", "business_org_name", "screen_name"]
        or_conditions = []
        for search_item in search_variables:
            or_conditions.append({search_item:reg_expression})

        type_list = ['unclaimed']
        type_list.extend(type_user_new)
        query_mongo = {'$or': or_conditions, 'sign_up_as': {'$in': type_list}, 'useruid': {'$nin': data_list}}
        mongo = MongoConnection("localhost",27017,'foodtrade')
        results = mongo.get_all('userprofile', query_mongo)
        
        final_organisation = []
        if len(results) == 0:
            final_organisation.append({'id': 'search', 'name': 'Search all users from twitter', 'screen_name': 'twitter',
             'profile_image_url_https':'https://pbs.twimg.com/profile_images/2284174758/v65oai7fxn47qv9nectx_bigger.png'})
        for each in results:
            if each.get('business_org_name')!=None:
                myname = each.get('business_org_name') if (each['sign_up_as'] == 'Business' or each['sign_up_as'] == 'Organisation') \
                and each.get('business_org_name')!='' else each['name']
            else:
                myname = each['name']                                            
            # final_organisation.append({'id': each['useruid'],
            #     'name':myname
            #     })
            final_organisation.append({'id': each['useruid'], 'name':myname, 'screen_name':each['screen_name'], 'profile_image_url_https':each['profile_img']})
        return HttpResponse(json.dumps(final_organisation))
    else:
        return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized to perform this action.'}))        

def get_banner_url(username=None, useruid=None, logged_useruid =None):
    # code to get profile banner url    
    banner_url = 'none'
    if banner_url != 'none':
        banner_url = banner_url+'/web_retina'

    else:
        try:
            if username!=None:
                account = SocialAccount.objects.get(user__username = username)
            elif useruid!=None:
                account = SocialAccount.objects.get(user__id = int(useruid))            
            banner_url = account.extra_data['profile_banner_url']
            banner_url = banner_url+'/web_retina'

        except:        
            try:
                friend_obj = Friends()
                if username!=None:
                    t_user = friend_obj.get_one({'friends.screen_name':username})
                if useruid != None:
                    t_user = friend_obj.get_one({'friends.id':useruid})        
                banner_url = t_user['friends']['profile_banner_url']
                banner_url = banner_url+'/web_retina'
            except:
                banner_url ='none'    
    return banner_url


def get_video_html(url):
    client = Embedly(settings.EMBEDLY_KEY)
    obj = client.oembed(url)

    if obj.get('error')==True:
        print 'error'
        return ''
    else:
        html = obj.get('html') if obj.get('html')!=None else ''
        width_start = html.find("width=\"") 
        width_end = html[width_start+7:].find('"')

        html = html.replace(html[width_start:(width_start+7+width_end+2)], "width=\"100%\"")

        height_start = html.find("height=\"") 
        height_end = html[height_start+7:].find('"')

        html = html.replace(html[height_start:(height_start+8+height_end+5)], "height=\"100%\"")
        return html

    

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
  
