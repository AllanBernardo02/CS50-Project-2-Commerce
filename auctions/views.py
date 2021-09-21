

from typing import Literal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render
from django.urls import reverse 
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
import os
from pytz import timezone

def index(request):
    listing = Listing.objects.all()
    return render(request, "auctions/index.html",{
        'listing': listing,

    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categ(request):
    return render(request, 'auctions/categories.html',{
        'category': Category.objects.all()
    })
    
def specific(request,cat_id):
    lis = Listing.objects.filter(category = cat_id)
    cat = Category.objects.get(pk = cat_id)
    return render(request, 'auctions/spec_category.html', {
        'catlist' :lis,
        'title' : cat,

    })
    
@login_required
def watchlist(request):
    user = User.objects.get(username=request.user)
    list = user.users_watchlist.all()
    if request.method == "POST":  # this will check if may pinasa si form/ or pag kinlick yung button
        listt = Listing.objects.get(pk = request.POST['remove'])
        user.users_watchlist.filter(list=listt).delete()
        return HttpResponseRedirect(reverse('watchlist'))
    apple = [ i.list for i in list ]
    return render(request, 'auctions/watchlist.html',{
        'listing': apple
    })
    
    
@login_required
def show_listing(request,list_id):
    listing = Listing.objects.get(pk = list_id)
    user = User.objects.get(username=request.user)
    if request.method == "POST":  # this will check if may pinasa si form
        if request.POST['button'] == "Watchlist":  # this will check the name of the button and its value 
            if not user.users_watchlist.filter(list= listing):  # this will check if the list is not already in the watchlist
               watch =  Watchlist(user = user, list = listing)
               watch.save()
            else:
                user.users_watchlist.filter(list=listing).delete()
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        if request.POST['button'] == "Place your Bid":
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.save(commit=False)  # meaning pwede mo pa imodify
                bid.user = user
                bid.save()
                new_bid = float(bid.bid)
                if listing.price >= new_bid:
                    return render(request, "auctions/listing.html", {
                            'list':listing,
                            'current_user':user,
                            'bidform':BidForm,
                            'comment': CommentForm,
                            "message": "Error! Invalid bid amount!"
                        })
                else:
                    listing.price = new_bid
                    listing.bid.add(bid)  # remember if its a foreignfield, you need the whole column to add 
                    listing.save()
                    
            else:
                return render(request, "auctions/listing.html", {
                            'list':listing,
                            'current_user':user,
                            'bidform':BidForm,
                            'comment': CommentForm,
                            "message": "10 digits max!!, 2 decimal places"
                        })
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))

        if request.POST['button'] == "Add Comment":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = user
                comment.save()
                listing.comment.add(comment)  # or set()
                listing.save()   
            else:
                return render(request, "auctions/listing.html", {
                            'list':listing,
                            'current_user':user,
                            'bidform':BidForm,
                            'comment': CommentForm,
                            "message": "10 digits max!!, 2 decimal places"
                        })             
        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    return render(request, 'auctions/listing.html', {
          'list':listing,
          'current_user':user,
          'bidform':BidForm,
          'comment': CommentForm,
          'message':''
         })
    



def create_listing(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = ListingForm(request.POST,request.FILES) #request.POST pag text and words lang pag request.FILES photos or any thing na need i upload also pag walang name si form matic yung value is naka store kay request.POST
        if form.is_valid():
            listt = form.save(commit=False)
            listt.user = user
            listt.save()
            return HttpResponseRedirect(reverse("create_listing"))
        else:
            return render(request, "auctions/create.html", {
                "form": form                # meaning pag may mali ibabalik mo yung form and didisplay niya yung mali
            })
    return render(request,'auctions/create.html',{
        'form' : ListingForm
    })
    
    
def show_my_listing(request):
    if request.method == 'POST':
        if request.POST.get('remove'):
            listing  = Listing.objects.get(pk = request.POST['remove'])
            if not listing.closed:
                listing.closed = True
                listing.save()
            else:
                listing.closed = False
                listing.save()
            return HttpResponseRedirect(reverse("user_listing"))
        if request.POST.get('delete'):
            listing  = Listing.objects.get(pk = request.POST['delete'])
            listing.bid.all().delete()
            listing.comment.all().delete()
            if listing.image is None:
                os.remove(listing.image.path)
            listing.delete()
            return HttpResponseRedirect(reverse("user_listing"))
            
    user = User.objects.get(username=request.user)
    user_listing = user.user_that_make_the_auction.all()
    return render(request, 'auctions/my_listing.html',{
        'listing':user_listing
    })
    