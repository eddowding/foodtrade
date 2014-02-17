"""
Wire this into the root URLConf this way::

    url(r'^stripe/', include('djstripe.urls', namespace="djstripe")),
    # url can be changed
    # Call to 'djstripe.urls' and 'namespace' must stay as is

Call it from reverse()::

    reverse("djstripe:subscribe")

Call from url tag::

    {% url 'djstripe:subscribe' %}

"""

from __future__ import unicode_literals
from django.conf.urls import patterns, url

from . import settings as app_settings
from . import views


urlpatterns = patterns("",

    # HTML views
    url(
        r"^$",
        views.AccountView.as_view(),
        name="account"
    ),
    url(
        r"^subscribe/$",
        views.SubscribeFormView.as_view(),
        name="subscribe"
    ),
    url(
        r"^change/plan/$",
        views.ChangePlanView.as_view(),
        name="change_plan"
    ),
    url(
        r"^change/cards/$",
        views.ChangeCardView.as_view(),
        name="change_card"
    ),
    url(
        r"^cancel/subscription/$",
        views.CancelSubscriptionView.as_view(),
        name="cancel_subscription"
    ),
    url(
        r"^history/$",
        views.HistoryView.as_view(),
        name="history"
    ),
    url(
        r"^admin/$",
        views.HistoryView.as_view(),
        name="admin_panel"
    ),
    url(
        r"^coupon$",
        views.CouponView.as_view(),
        name="add_coupon"
    ),
    url(
        r"^coupon/add$",
        views.AddCoupon.as_view(),
        name="add_coupon"
    ),
    url(
        r"^apply_coupon$",
        views.ApplyCoupon.as_view(),
        name="apply_coupon"
    ),


    # Web services
    url(
        r"^a/sync/history/$",
        views.SyncHistoryView.as_view(),
        name="sync_history"
    ),
    url(
        r"^a/check/available/(?P<attr_name>(username|email))/$",
        views.CheckAvailableUserAttributeView.as_view(),
        name="check_available_user_attr"
    ),

    # Webhook
    url(
        app_settings.DJSTRIPE_WEBHOOK_URL,
        views.WebHook.as_view(),
        name="webhook"
    ),

)