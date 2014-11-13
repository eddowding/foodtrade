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
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    distance = request.GET.get('distance')
    if request.user.is_authenticated():
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(request.user.id))
        if user_profile.get('latlng') and user_profile.get('latlng').get('coordinates'):
            lat = user_profile.get('latlng').get('coordinates')[1]
            lng = user_profile.get('latlng').get('coordinates')[0]
            distance = '20km'
    sqs = S().indexes(settings.ES_INDEX).query(_all__fuzzy=query)
    if lat and lng:
        sqs = sqs.filter(latlng__distance=(distance, lat, lng))
    html = render_to_string('_partials/search_result.html', {'sqs': sqs}, context_instance=RequestContext(request))
    objs = list(sqs.values_dict('id', 'name', 'profile_image', 'description', 'latlng'))
    return HttpResponse(json.dumps({'html': html, 'objs': objs}))
