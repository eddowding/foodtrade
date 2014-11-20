from django.conf.urls import patterns, url

urlpatterns = patterns('tools.views',
    url(r'^$', 'location_tool', name='location_tool'),
    url(r'location/save/$', 'location_tool_operation', name='location_tool_operation'),
)
