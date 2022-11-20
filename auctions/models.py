from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class userProfile(models.Model):
    user = models.OneToOneField('auctions.User', null=True,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,null=True, blank=True)
    user_address = models.CharField(max_length=30, null=True, blank=True)


class User(AbstractUser):
    pass

class CategoryList(models.Model):
    category_list = models.CharField(max_length=64)
    category_url = models.CharField(max_length=64)

class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    athlete_name=models.CharField(max_length=64, null=True, blank=True)
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64)
    image_file = models.ImageField(upload_to="files/product_images" ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_bids = models.IntegerField(default = 0)


class Bid(models.Model):
    user = models.CharField(max_length=64)
    email  = models.CharField(max_length=254)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()
    athlete_name = models.CharField(max_length=64)
    phone_number=models.CharField(max_length=10,null=True, blank=True)


class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()


class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()
    title = models.CharField(max_length=64, null=True)
    athlete_name = models.CharField(max_length=64)
