from django.conf.urls import patterns, url

urlpatterns = patterns('menu.views',
    url(r'^$', 'menu', name='menu'),
    url(r'^login/$', 'login', name='menu-login'),
    url(r'register/$', 'register', name='menu_register'),
    url(r'user/lookup/count/$', 'user_lookup_count', name='menu_user_lookup_count'),
    url(r'^logout/$', 'logout', name='menu_logout'),
    url(r'^establishment/lookup/name/$', 'establishment_lookup_name', name='menu_establishment_lookup_name'),
    url(r'^create/menu/$', 'create_menu', name='menu_create_menu'),
    url(r'^create/menu/section/$', 'create_menu_section', name='menu_create_menu_section'),
    url(r'^create/dish/$', 'create_dish', name='menu_create_dish'),
    url(r'^create/ingredient/$', 'create_ingredient', name='menu_create_ingredient'),
    url(r'^update/ingredient/$', 'update_ingredient', name='menu_update_ingredient')
)
