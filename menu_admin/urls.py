from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('menu_admin.views',
    url(r'^user/$', 'admin_user', name='menu_admin_user'),
    url(r'^user/(?P<id>[\w]+)/$', 'admin_user_detail', name='menu_admin_user_detail'),
    url(r'^user/(?P<id>[\w]+)/update/$', 'admin_user_detail_update', name='menu_admin_user_detail_update'),
    url(r'^dish/$', 'admin_dish', name='menu_admin_dish'),
    url(r'^dish/(?P<id>[\w]+)/$', 'admin_dish_detail', name='menu_admin_dish_detail'),
    url(r'^dish/(?P<id>[\w]+)/update/$', 'admin_dish_detail_update', name='menu_admin_dish_detail_update'),
    url(r'^ingredient/$', 'admin_ingredient', name='menu_admin_ingredient'),
    url(r'^ingredient/(?P<id>[\w]+)/$', 'admin_ingredient_detail', name='menu_admin_ingredient_detail'),
    url(r'^ingredient/(?P<id>[\w]+)/update/$', 'admin_ingredient_detail_update', name='menu_admin_ingredient_detail_update'),
)
