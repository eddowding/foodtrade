from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from mainapp.forms import PassworResetForm
admin.autodiscover()
# handler404 = 'mainapp.views.my_404_view'
urlpatterns = patterns('',
    url(r'^$', 'mainapp.home.home', name='home'),
    url(r'^kpi/$', 'mainapp.kpi.stats'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',content_type='text/plain'), name='robots'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),
    url(r'^admin-tags$', 'mainapp.home.admin_tags', name='home'),
    url(r'^food-tags$', 'mainapp.home.food_tags', name='home'),
    url(r'^ajax-handler/(?P<func_name>\w{1,40})$', 'mainapp.home.ajax_request', name='ajax_handle'),
    url(r'^tweets/$', 'mainapp.views.tweets', name='home'),
    url(r'^activity/$', 'mainapp.activity.home', name='home'),
    url(r'^(?i)profile/(?P<username>[-\w]+)/$', 'mainapp.profilepage.resolve_profile_display', name='resolve_profile'),
    url(r'^(?i)person/(?P<username>[-\w]+)/$', 'mainapp.profilepage.resolve_profile_display', name='profile'),
    url(r'^(?i)business/(?P<username>[-\w]+)/$', 'mainapp.profilepage.resolve_profile_display', name='profile'),
    url(r'^(?i)organisation/(?P<username>[-\w]+)/$', 'mainapp.profilepage.resolve_profile_display', name='profile'),
    url(r'^(?i)unclaimed/(?P<username>[-\w]+)/$', 'mainapp.profilepage.resolve_profile_display', name='profile'),
    # url(r'^foodtrade/', include('foodtrade.foo.urls')),


    # (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    # (r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
    #  {'post_reset_redirect' : '/accounts/password/done/'}),
    # (r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

#     url(r'^accounts/password/reset/confirm/$',
#              'django.contrib.auth.views.password_reset_confirm', name="auth_password_reset_confirm"),
#     url(r'^accounts/password/reset/complete/$',
#              'django.contrib.auth.views.password_reset_complete'),
    # url(r'^accounts/password/change/$', 'mainapp.views.my_password_change ', name='my_password_change '),


    url(r'^accounts/social/signup/', 'mainapp.signup_views.signup_view', name = 'account_signup'),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts/signup/', 'mainapp.signup_views.signup_view_new'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^(?i)editprofile/(?P<username>[-\w]+)/$','mainapp.profilepage.edit_profile'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mongonaut/', include('mongonaut.urls')),
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
    url(r'^mailchimp-migrate/(?P<username>\w{1,40})/$', 'mainapp.views.transport_mailchimp'),
    url(r'^send-newsletter/(?P<substype>[-\w]+)/$', 'mainapp.views.send_newsletter'),
    url(r'^payments/', include('djstripe.urls', namespace="djstripe")),
    url(r'^twillo/$', 'mainapp.views.sms_receiver'),
    url(r'^all_users/$', 'mainapp.home.all_users'),
    url(r'^twitteruser/queries/$', 'mainapp.twitter_search.search_users'),
    url(r'^queries/(?P<type_user>[-\w]+)/$', 'mainapp.profilepage.search_orgs_business'),
    # Temporary urls
    url(r'^merge-data/$', 'mainapp.merge_data.merge'),
    url(r'^update-image/$', 'mainapp.merge_data.update_image'),
    url(r'^visitors/$', 'mainapp.profilepage.get_views_count'),
    # url(r'^activity/(?P<request_type>\w{1,40})$', 'mainapp.activity.activity_suppliers'),
    url(r'^myprofile/favourites/$', 'mainapp.favpage.display_favourites'),
    ## any search views
    url(r'^search/', include('search.urls')),
    url(r'^tools/', include('tools.urls')),
    url(r'^menu/', include('menu.urls'))
)
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns('',
        (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
     {'post_reset_redirect' : '/accounts/password/reset/done/','password_reset_form':PassworResetForm, 'template_name': 'account/password_reset.html'}),)
urlpatterns += patterns('',
        url(r'^accounts/', include('allauth.urls')),)

urlpatterns += patterns('',
        url(r'^(?P<username>\w{1,40})/$', 'mainapp.profilepage.profile_url_resolve'), )
