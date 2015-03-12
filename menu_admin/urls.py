from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('menu_admin.views',
    url(r'^user/$', 'admin_user', name='menu_admin_user'),
    url(r'^user/(?P<id>[\w]+)/$', 'admin_user_detail', name='menu_admin_user_detail'),
)
