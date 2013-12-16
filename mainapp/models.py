from django.db import models

# Create your models here.
class MaxTweetId(models.Model):
    """docstring for MaxTweetId"""
    max_tweet_id =  models.CharField(max_length = 50, unique = True)
    def __unicode__(self):
        return self.max_tweet_id