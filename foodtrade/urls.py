from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mainapp.home.home', name='home'),
    url(r'^admin-tags$', 'mainapp.home.admin_tags', name='home'),
    url(r'^ajax-handler/(?P<func_name>\w{1,40})$', 'mainapp.home.ajax_request', name='ajax_handle'),
    url(r'^tweets/$', 'mainapp.views.tweets', name='home'),
    url(r'^activity/$', 'mainapp.activity.home', name='home'),
    url(r'^register/$', 'mainapp.views.register', name='register'),
    url(r'^singlebusiness/$', 'mainapp.views.singlebusiness', name='singlebusiness'),
    # url(r'^foodtrade/', include('foodtrade.foo.urls')),
    url(r'^accounts/', include('allauth.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
