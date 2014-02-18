from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mainapp.home.home', name='home'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',content_type='text/plain'), name='robots'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),

    url(r'^admin-tags$', 'mainapp.home.admin_tags', name='home'),
    url(r'^food-tags$', 'mainapp.home.food_tags', name='home'),
    url(r'^ajax-handler/(?P<func_name>\w{1,40})$', 'mainapp.home.ajax_request', name='ajax_handle'),
    url(r'^tweets/$', 'mainapp.views.tweets', name='home'),
    url(r'^activity/$', 'mainapp.activity.home', name='home'),
    url(r'^profile/(?P<username>[-\w]+)/$', 'mainapp.profilepage.resolve_profile', name='resolve_profile'),
    url(r'^person/(?P<username>[-\w]+)/$', 'mainapp.profilepage.display_profile', name='profile'),
    url(r'^business/(?P<username>[-\w]+)/$', 'mainapp.profilepage.display_profile', name='profile'),
    url(r'^organisation/(?P<username>[-\w]+)/$', 'mainapp.profilepage.display_profile', name='profile'),
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
    url(r'^pages/(?P<page_name>\w{1,40})$', 'mainapp.pricing.pages'),
    # url(r'^privacy/', 'mainapp.privacy.home'),
    # url(r'^terms/', 'mainapp.terms.home')

    url(r'^invite/$', 'mainapp.views.invite'),
    url(r'^invitation/(?P<invite_id>\w{1,40})/$', 'mainapp.views.handle_invitation_hit', name='handle_invitation_hit'),
    url(r'^pricing/$', 'mainapp.pricing.home'),
    url(r'^inbox/$', 'mainapp.views.notifications'),
    url(r'^unclaimed-profiles/', 'mainapp.views.unclaimed_profiles'),
    url(r'^(?P<username>[-\w]+)/post/(?P<tweet_id>[-\w]+)/$', 'mainapp.single_activity.home', name='single_activity'),
    url(r'^mailchimp-migrate/$', 'mainapp.views.transport_mailchimp'),
    url(r'^send-newsletter/$', 'mainapp.views.send_newsletter'),
    url(r'^twillo/$', 'mainapp.views.sms_receiver'),
)
