from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import *

#creating forms
class ListingForm(ModelForm):
    class Meta:
        model = Listing    
        fields =  ['title', 'price', 'category' ,'image']         #"__all__" shortcut para lahat na agad
        
        
        
        
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']