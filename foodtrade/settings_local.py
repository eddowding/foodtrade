# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# For Django All Auth
SITE_ID = 1
#LOGIN_REDIRECT_URL=""
# FACEBOOK_APP_ID = '127413947360910',
# FACEBOOK_APP_SECRET = '24216b766f2e2a2bd532fbae48845b60'
# FACEBOOK_PROFILE_ID = '1741776904'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
SOCIALACCOUNT_AUTO_SIGNUP = True
LOGIN_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_FORM_CLASS = 'mainapp.forms.SignupForm'
ACCOUNT_LOGOUT_ON_GET = True



# For mail server
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025