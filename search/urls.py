from django.conf.urls import patterns, url

urlpatterns = patterns('search.views',
    url(r'^$', 'search', name='search'),
)
