from django.conf.urls import patterns, url

urlpatterns = patterns('menu.views',
    url(r'^$', 'menu', name='menu'),
    url(r'^register/$', 'register', name='menu-registration'),
    url(r'^login/$', 'login', name='menu-login')
)
