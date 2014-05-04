from django.shortcuts import render_to_response
from django.template import RequestContext
from mainapp.classes.TweetFeed import UserProfile
from django.contrib.auth.decorators import login_required
from classes.DataConnector import UserInfo

@login_required(login_url='/')
def display_favourites(request):
    parameters={}
    user_prof = UserProfile()
    user_id = request.user.id
    prof = user_prof.get_profile_by_id(user_id)
    fav_users = prof.get('favourites')
    user_info = UserInfo(user_id)
    parameters['userinfo'] = user_info
    if fav_users!=None:
        fav_users_list = []
        for each_usr in fav_users:
            prof = user_prof.get_profile_by_id(request.user.id)
            fav_users_list.append(prof)
        parameters['fav_users_list'] = fav_users_list
    return render_to_response('favourites.html', parameters, context_instance=RequestContext(request))

def get_views_parameters(request, find_username):
    from mainapp.classes.Search import Search
    parameters={}
    user_profile_obj = UserProfile()
    parameters.update(csrf(request))

    if request.user.is_authenticated():
        user_id = request.user.id
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        default_lon = float(user_profile['latlng']['coordinates'][0])
        default_lat = float(user_profile['latlng']['coordinates'][1])
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        location_info = get_addr_from_ip(ip)
        default_lon = float(location_info['longitude'])
        default_lat = float(location_info['latitude'])

    from mainapp.classes.profilevisits import ProfileVisits    
    profile_visits_obj = ProfileVisits()
    visit_stats = profile_visits_obj.get_visit_stats(pagenum=1,
        conditions={'profile_name':{ "$regex" : re.compile("^"+str(find_username)+"$", re.IGNORECASE), "$options" : "-i" }})
    find_user = user_profile_obj.get_profile_by_username(find_username)

    results = []
    for eachVisit in visit_stats:
        data={}
        if eachVisit['visitor_name']!='':
            data['username'] = eachVisit['visitor_name']
        else:
            data['username'] = 'Unknown visitor'

        if eachVisit['visitor_name'] == '':
            continue
        chk_usr = user_profile_obj.get_profile_by_username(eachVisit['visitor_name'])
        data['profile_img'] = chk_usr['profile_img']
        data['address'] = chk_usr['address']
        data['latitude'] = chk_usr['latlng']['coordinates'][1]
        data['longitude'] = chk_usr['latlng']['coordinates'][0]
        data['sign_up_as'] = chk_usr['sign_up_as']
        data['name'] = chk_usr['name']
        data['useruid'] = chk_usr['useruid']
        data['description'] = chk_usr['description']
        try:
            if chk_usr['subscribed'] ==1:
                data['subscribed'] = True
            else:
                data['subscribed'] = False            
        except:
            data['subscribed'] = False

        if chk_usr['sign_up_as'] == 'Individual':
            data['result_class'] = 'individual updates'
        elif chk_usr['sign_up_as'] == 'Organisation':
            data['result_class'] = 'organisation updates'
        else:
            data['result_class'] = 'business updates'        
        
        data['distance_text'] = str(distance(default_lon, default_lat, chk_usr['latlng']['coordinates'][0], chk_usr['latlng']['coordinates'][1])) + ' miles away'
        time_elapsed = int(time.time()) -eachVisit['visit_time']
        if time_elapsed<60:
            time_text = str(time_elapsed) + ' seconds ago'
        elif time_elapsed < 3600:
            minutes = time_elapsed/60
            time_text = str(minutes) + ' minutes ago'
        elif time_elapsed < 3600*24:
            hours = time_elapsed/3600
            time_text = str(hours) + ' hours ago'
        elif time_elapsed < 3600*24*365:
            days = time_elapsed/3600/24
            time_text = str(days) + ' days ago'
        else:
            years = time_elapsed/3600/24/365
            time_text = str(years) + ' years'
        data['visit_time'] = time_text
        data['visit_date_time'] = str(datetime.datetime.fromtimestamp(int(eachVisit['visit_time'])))
        results.append(data)
    parameters['results'] = results
    parameters['visit_data'] = str(json.dumps(results))
    return parameters   