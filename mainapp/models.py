from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
# Create your models here.

class User(models.Model):

    """ Custom fields go here """

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    @cached_property
    def has_active_subscription(self):
        """
        Helper property to check if a user has an active subscription.
        """
        # Anonymous users return false
        if self.is_anonymous():
            return False

        # Import placed here to avoid circular imports
        from djstripe.models import Customer

        # Get or create the customer object
        customer, created = Customer.get_or_create(self)

        # If new customer, return false
        # If existing customer but inactive return false
        if created or not customer.has_active_subscription():
            return False

        # Existing, valid customer so return true
        return True


class MaxTweetId(models.Model):
    """docstring for MaxTweetId"""
    max_tweet_id =  models.CharField(max_length = 50, unique = True)
    def __unicode__(self):
        return str(self.max_tweet_id)


class FoodPhoto(models.Model):
    """ Model just for uploading images to media dir"""
    food_photo = models.ImageField(upload_to='food/')





