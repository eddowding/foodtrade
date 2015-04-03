from django.conf.urls import patterns, url


urlpatterns = patterns('menu_admin.views',
    url(r'^user/$', 'admin_user', name='menu_admin_user'),
    url(r'^user/(?P<id>[\w]+)/$', 'admin_user_detail', name='menu_admin_user_detail'),
    url(r'^user/(?P<id>[\w]+)/update/$', 'admin_user_detail_update', name='menu_admin_user_detail_update'),
    url(r'^user/(?P<id>[\w]+)/delete/$', 'admin_user_delete', name='menu_admin_user_delete'),

    url(r'^dish/$', 'admin_dish', name='menu_admin_dish'),
    url(r'^dish/(?P<id>[\w]+)/$', 'admin_dish_detail', name='menu_admin_dish_detail'),
    url(r'^dish/(?P<id>[\w]+)/update/$', 'admin_dish_detail_update', name='menu_admin_dish_detail_update'),
    url(r'^dish/(?P<id>[\w]+)/delete/$', 'admin_dish_delete', name='menu_admin_dish_delete'),

    url(r'^ingredient/$', 'admin_ingredient', name='menu_admin_ingredient'),
    url(r'^ingredient/(?P<id>[\w]+)/$', 'admin_ingredient_detail', name='menu_admin_ingredient_detail'),
    url(r'^ingredient/(?P<id>[\w]+)/update/$', 'admin_ingredient_detail_update', name='menu_admin_ingredient_detail_update'),
    url(r'^ingredient/(?P<id>[\w]+)/delete/$', 'admin_ingredient_detail_delete', name='menu_admin_ingredient_detail_delete'),

    url(r'^establishment/$', 'admin_establishment', name='menu_admin_establishment'),
    url(r'^establishment/(?P<id>[\w]+)/$', 'admin_establishment_detail', name='menu_admin_establishment_detail'),
    url(r'^establishment/(?P<id>[\w]+)/update/$', 'admin_establishment_detail_update', name='menu_admin_establishment_detail_update'),
    url(r'^establishment/(?P<id>[\w]+)/delete/$', 'admin_establishment_delete', name='menu_admin_establishment_delete'),

    url(r'^meat/$', 'admin_meat', name='menu_admin_meat'),
    url(r'^meat/(?P<id>[\w]+)/$', 'admin_meat_detail', name='menu_admin_meat_detail'),
    url(r'^meat/(?P<id>[\w]+)/update/$', 'admin_meat_detail_update', name='menu_admin_meat_detail_update'),
    url(r'^meat/(?P<id>[\w]+)/delete/$', 'admin_meat_delete', name='menu_admin_meat_delete'),

    url(r'^allergen/$', 'admin_allergen', name='menu_admin_allergen'),
    url(r'^allergen/(?P<id>[\w]+)/$', 'admin_allergen_detail', name='menu_admin_allergen_detail'),
    url(r'^allergen/(?P<id>[\w]+)/update/$', 'admin_allergen_detail_update', name='menu_admin_allergen_detail_update'),
    url(r'^allergen/(?P<id>[\w]+)/delete/$', 'admin_allergen_delete', name='menu_admin_allergen_delete'),

    url(r'^bulk/delete/(?P<type>[\d]+)/$', 'admin_bulk_delete', name='menu_admin_bulk_delete')
)
