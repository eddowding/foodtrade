from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mainapp.home.home', name='home'),
    url(r'^admin-tags$', 'mainapp.home.admin_tags', name='home'),
    url(r'^ajax-handler/(?P<func_name>\w{1,40})$', 'mainapp.home.ajax_request', name='ajax_handle'),
    url(r'^tweets/$', 'mainapp.views.tweets', name='home'),
    url(r'^activity/$', 'mainapp.activity.home', name='home'),
    url(r'^profile/(?P<username>[-\w]+)/$', 'mainapp.profilepage.display_profile', name='profile'),
    # url(r'^foodtrade/', include('foodtrade.foo.urls')),
    url(r'^accounts/social/signup/', 'mainapp.signup_views.signup_view', name = 'account_signup'),
    url(r'^accounts/', include('allauth.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^editprofile/(?P<username>[-\w]+)/$','mainapp.profilepage.edit_profile'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^trends/', 'mainapp.views.trends'),
    url(r'^pricing/', 'mainapp.pricing.home'),
    # url(r'^privacy/', 'mainapp.privacy.home'),
    # url(r'^terms/', 'mainapp.terms.home')
)
