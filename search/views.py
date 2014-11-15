import json
from elasticutils import S
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from mainapp.classes.TweetFeed import UserProfile


def search(request):
    return render(request, 'search.html')

def search_result(request): #TODO: change result div name, change hard coded url.
    query = request.GET.get('query')
    lat = float(request.GET.get('lat')) if request.GET.get('lat') else None
    lng = float(request.GET.get('lng')) if request.GET.get('lng') else None
    distance = request.GET.get('distance')
    if request.user.is_authenticated():
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(request.user.id))
        if user_profile.get('latlng') and user_profile.get('latlng').get('coordinates'):
            lat = user_profile.get('latlng').get('coordinates')[1]
            lng = user_profile.get('latlng').get('coordinates')[0]
            distance = '20km'
    sqs = S().indexes(settings.ES_INDEX).query(_all__fuzzy=query).facet('sign_up_as')
    if lat and lng:
        sqs = sqs.filter(latlng__distance=(distance, lat, lng))
    html = render_to_string('_partials/search_result.html', {'sqs': sqs}, context_instance=RequestContext(request))
    objs = list(sqs.values_dict('id', 'name', 'profile_img', 'description', 'latlng', 'username'))
    facets = {}#TODO: check why this iteration is required
    for k, v in sqs.facet_counts().items():
        facets[k] = {'total': v['total'], 'terms': v['terms']}
    return HttpResponse(json.dumps({'html': html, 'objs': objs, 'facets': facets}))
