from typing import AbstractSet
from django import forms
from django.forms import widgets
from .models import *

class CreateListForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'starting_bid', 'image' ]

        widgets = {
            'image': forms.TextInput(attrs={'placeholder': 'Enter the URl of your image here'}),
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Product description'}),
            'starting_bid': forms.NumberInput(attrs={'placeholder': 'Starting Bid'}),

        }

        labels = {
            'title': '',
            'description': '',
            'starting_bid': '',
            'image': ''
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

        labels = {'bid': ''}

        widgets = {
            'bid': forms.NumberInput(attrs={'placeholder': '0.0'})
        }