from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MaxTweetId(models.Model):
    """docstring for MaxTweetId"""
    max_tweet_id =  models.CharField(max_length = 50, unique = True)
    def __unicode__(self):
        return str(self.max_tweet_id)
