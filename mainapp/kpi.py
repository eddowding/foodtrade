from django.shortcuts import render_to_response
from django.template import RequestContext
from mainapp.classes.TweetFeed import UserProfile, KPI
from mainapp.classes.KpiClass import KPIStats

def stats(request):
    parameters = {}
    user_prof = UserProfile()
    stats = KPIStats()
    parameters['user_count'] = stats.user_count()
    parameters['total_connections'] = stats.total_connections()
    parameters['connections_per_business'] = stats.avg_conn_per_business()
    parameters['total_activity'] = stats.activity_count()
    parameters['total_replies'] = stats.replies_count()
    kpi_obj = KPI()
    kpi_obj.create_kpi(parameters)
    print "KPI saved"
    return render_to_response('kpi.html', parameters, context_instance=RequestContext(request))