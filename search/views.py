import json
from elasticutils import S
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from mainapp.classes.TweetFeed import UserProfile


def search(request):
    if request.user.is_authenticated():
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(request.user.id))
        print user_profile
    return render(request, 'search.html')

def search_result(request): #TODO: change result div name, change hard coded url.
    query = request.GET.get('query')
    sqs = S().indexes(settings.ES_INDEX).query(_all__fuzzy=query)
    html = render_to_string('_partials/search_result.html', {'sqs': sqs}, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({'html': html}))
