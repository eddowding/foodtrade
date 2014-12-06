from django.conf.urls import patterns, url

urlpatterns = patterns('menu.views',
    url(r'^$', 'menu', name='menu'),    
    url(r'^login/$', 'login', name='menu-login'),
    url(r'register/$', 'register', name='menu_register'),
    url(r'user/lookup/count/$', 'user_lookup_count', name='menu_user_lookup_count')

)
