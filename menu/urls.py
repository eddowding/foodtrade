from django.conf.urls import patterns, url

urlpatterns = patterns('menu.views',
    url(r'^$', 'menu', name='menu')
)
