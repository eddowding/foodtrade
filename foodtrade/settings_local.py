# -*- coding: utf-8 -*-
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# app credentials
import os
from mongoengine import connect


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

CONSUMER_KEY = 'waBmigQf9LIqYXkhMNeMdQ'
CONSUMER_SECRET = 'KVVf35OAJQVUGrVQsrQnF7fmB2JLz6XAW3IAmqFB8'

#new ones of foodtrade_help  -- only to use for reply messages
BOT_ACCESS_TOKEN = '2304652134-1IvED7AvT9vPeSxILY3GmaanySroansD28Sl4n7'
BOT_ACCESS_TOKEN_SECRET = '9Hb8qd7OQfYDTt4fgl113Xue0hopbFbwkIA94E0X2PZBs'

#new ones of foodtradeHQ  -- to use with daemon.. msg parsing
HQ_ACCESS_TOKEN = '384361932-BdKtwhhRDILj4YeHU1G3UN1QtvlrD8LfsqsK6lDF'
HQ_ACCESS_TOKEN_SECRET = 'xGB1Wl4kHnBdxZIDufXTKDQNZPPxbj3PWjMTqH4X802mr'

#..................Server Settings............................
REMOTE_SERVER_LITE = 'foodtradelite.cloudapp.net'
LOCAL_SERVER = 'localhost'
REMOTE_SERVER_STAGING = 'ftstaging.cloudapp.net'
REMOTE_MONGO_DBNAME = 'foodtrade'
REMOTE_MONGO_USERNAME = 'ftroot'
REMOTE_MONGO_PASSWORD = 'ftroot'
#..................Server Settings............................

EMBEDLY_KEY = 'dda65dba82724765b3b82e79525286cc'

# old ones of my twitter app
# CONSUMER_KEY = 'seqGJEiDVNPxde7jmrk6dQ'
# CONSUMER_SECRET = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'

import os
# Test stripe account from sujit
# STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_cIjJbOYUbVYnvnSn1QyeMD7r")
# STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_dj0ArFwwcCljH8n1aioJ6jtV")


# # Test stripe account from Ed
# STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_oSOpaxq2GleFxB6MBelA5S3o")
# STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_hmGuDVayPPKB81MKCPKnyfK1")

# live stripe account from Ed
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_live_9BlCZzoxIYjEPaIdwBWLjRjR")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_live_nobdUwMzfapMBkwn3CKcD0Eg")

DJSTRIPE_PLANS = {

    "yearly": {
        "stripe_plan_id": "business-yearly",
        "name": "Basic (£45 / yr)",
        "description": "The annual subscription plan to FoodTrade",
        "price": 4500,  # £19900
        "currency": "gbp",
        "interval": "year"
    }
}




# old ones of myfoodtrade
# admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
# admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'


# For Django All Auth
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
SOCIALACCOUNT_AUTO_SIGNUP = True
LOGIN_REDIRECT_URL = "/activity/"
ACCOUNT_SIGNUP_FORM_CLASS = 'mainapp.forms.SignupForm'
ACCOUNT_LOGOUT_ON_GET = True


# ACCOUNT_SIGNUP_FORM_CLASS = "djstripe.forms.StripeSubscriptionSignupForm"
DEFAULT_FROM_EMAIL = 'FoodTrade <noreply@foodtrade.com>'
REMOVE_WWW = False


#elastic search settings for utils
ES_URLS = ['http://localhost:9200']
ES_INDEX = 'foodtrade'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'foodtrade'
MONGO_USER = None
MONGO_PASS = None

connect(db=MONGO_DB, host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USER, password=MONGO_PASS)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

#bower settings
BOWER_COMPONENTS_ROOT = PROJECT_ROOT
BOWER_INSTALLED_APPS = ('typeahead.js#0.10.5',
 'jquery-sortable#0.9.12',
 'jquery#1.11.1',
 'x-editable#1.5.1')

#cache backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
