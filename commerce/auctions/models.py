
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from dateutil import tz
class User(AbstractUser):
    pass

# --run-syncdb


class Listing(models.Model):
    user = models.ForeignKey('User', on_delete=CASCADE, related_name='user_that_make_the_auction')
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey('Category', on_delete=CASCADE, related_name='selected_category',blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(null = True, blank = True, upload_to = 'images/')
    closed = models.BooleanField(default=False)
    bid = models.ManyToManyField('Bid', blank=True, related_name='listing_bid')
    comment = models.ManyToManyField('Comment',blank=True, related_name='list_comment')
    
    
    def __str__(self):
        return f"{self.title}: sold for {self.price} by {self.user}"


class Category(models.Model):
    Cat_name = models.CharField(max_length=50)    

    
    def __str__(self):
        return f"{self.Cat_name}"


class Watchlist(models.Model):
    user = models.ForeignKey('User',on_delete=CASCADE, related_name= "users_watchlist")
    list = models.ForeignKey('Listing', on_delete=CASCADE,related_name='Watchlist')
    
    def __str__(self):
              return f"{self.user.username} listed {self.list.title}"


class Bid(models.Model):
     user = models.ForeignKey('User', on_delete=CASCADE,related_name='user_bid')
     bid = models.DecimalField(max_digits=10, decimal_places=2)
     
     def __str__(self):
         return f"${self.bid} by {self.user}"
     
     
     
class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=CASCADE, related_name='user_comment')
    time = models.DateTimeField(auto_now_add=True, blank=True)
    comment = models.CharField(max_length=200)
    
    
    def __str__(self):
        return f"{self.comment}  by: {self.user}"