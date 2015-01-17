from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('menu.views',
    #common
    url(r'^$', 'dashboard', name='menu_dashboard'),
    url(r'^menu/$', 'menu', name='menu'),
    url(r'^login/$', 'login', name='menu-login'),
    url(r'register/$', 'register', name='menu_register'),
    url(r'user/lookup/count/$', 'user_lookup_count', name='menu_user_lookup_count'),
    url(r'^logout/$', 'logout', name='menu_logout'),

    #menu
    url(r'^establishment/lookup/name/$', 'establishment_lookup_name', name='menu_establishment_lookup_name'),
    url(r'^create/menu/$', 'create_menu', name='menu_create_menu'),
    url(r'^delete/menu/$', 'delete_menu', name='menu_delete_menu'),
    url(r'^create/menu/section/$', 'create_menu_section', name='menu_create_menu_section'),
    url(r'^delete/menu/section/$', 'delete_menu_section', name='menu_delete_menu_section'),
    url(r'^dish/lookup/name/$', 'dish_lookup_name', name='menu_dish_lookup_name'),
    url(r'^create/dish/$', 'create_dish', name='menu_create_dish'),
    url(r'^update/dish/$', 'update_dish', name='menu_update_dish'),
    url(r'^delete/dish/$', 'delete_dish', name='menu_delete_dish'),
    url(r'^create/ingredient/$', 'create_ingredient', name='menu_create_ingredient'),
    url(r'^update/ingredient/$', 'update_ingredient', name='menu_update_ingredient'),
    url(r'^update/ingredient/name/$', 'update_ingredient_name', name='menu_update_ingredient_name'),
    url(r'^delete/ingredient/$', 'delete_ingredient', name='menu_delete_ingredient'),
    url(r'^ingredient/lookup/name/$', 'ingredient_lookup_name', name='menu_ingredient_lookup_name'),
    url(r'^ingredient/save/moderation/$', 'save_moderation_ingredient', name='menu_save_moderation_ingredient'),
    url(r'^ingredient/update/moderation/$', 'update_moderation_ingredient', name='menu_update_moderation_ingredient'),

    #print
    url(r'^preview/(?P<id>[\w]+)$', 'print_preview_menu', name='menu_print_preview_menu'),

    #connection
    url(r'^connection/$', 'connection', name='menu_connection'),
    url(r'^create/connection/$', 'create_connection', name='menu_create_connection')


)
# if settings.DEBUG:
#     urlpatterns += patterns('',
#     ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
