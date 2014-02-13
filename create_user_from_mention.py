import Twython

t = Twython(app_key=settings.TWITTER_CONSUMER_KEY,
            app_secret=settings.TWITTER_CONSUMER_SECRET,
            oauth_token=oauth_token,
            oauth_token_secret=oauth_token_secret)

print t.show_user(screen_name=account_name)