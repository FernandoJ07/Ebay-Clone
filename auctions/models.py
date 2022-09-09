from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BLANK_CHOICE_DASH, related

class User(AbstractUser):
    pass


category_options= [
	(0, 'Electronic'),
	(1, 'Clothes'),
	(2, 'Toys')
]

class Listing(models.Model):

	title = models.CharField(max_length=64)
	description = models.TextField()
	category = models.IntegerField(choices=category_options)
	starting_bid = models.IntegerField()
	bids = models.ManyToManyField('Bid', related_name='bidsListing', blank=True)
	active = models.BooleanField(default=True)
	image = models.CharField(max_length=200)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

	def __str__(self):
		return self.title


class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
	listings = models.ManyToManyField(Listing, blank=True, related_name='listings_watchlist')

	def __str__(self): 
		return f'{self.user.username}'

class Bid(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listings_bid')
	bid = models.FloatField()
	bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bid")

	def __str__(self):
		return f"{self.bid} for {self.bidder}"

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userComment')
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listingComment')
	comment = models.TextField()

	def __str__(self):
		return f'Comment for "{self.user}" in "{self.listing}"'
	