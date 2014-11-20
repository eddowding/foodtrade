from django.conf.urls import patterns, url

urlpatterns = patterns('tools.views',
    url(r'^$', 'location_tool', name='location_tool'),
)
