from django.conf.urls import patterns, url

urlpatterns = patterns('menu.views',
    url(r'^$', 'menu', name='menu'),
    url(r'^login/$', 'login', name='menu-login'),
    url(r'register/$', 'register', name='menu_register'),
    url(r'user/lookup/count/$', 'user_lookup_count', name='menu_user_lookup_count'),
    url(r'^logout/$', 'logout', name='menu_logout'),
    url(r'^establishment/lookup/name/$', 'establishment_lookup_name', name='menu_establishment_lookup_name')
)
