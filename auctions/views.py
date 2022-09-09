from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.forms.widgets import NumberInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect   
from django.urls import reverse

from .models import *
from .forms import *



def index(request):

    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        'listings': listings
    })

def listing(request, id):

    listing = Listing.objects.filter(id = id)

    try:
        my_watchlist = Watchlist.objects.get(user=request.user)
    except:
        my_watchlist = False

    # show information about bids
    total_bids =  Bid.objects.filter(listing = id).count()

    if total_bids > 0:
        last_bid = Bid.objects.filter(listing = id)[total_bids-1]

    else:
        last_bid = Bid.objects.filter(listing = id)

    try:
        myLastBid = Bid.objects.filter(listing = id, bidder = request.user).last()
    except:
        myLastBid = False
    # --------------------------------

    return render(request, 'auctions/listing.html', {
        'listing': listing, 
        "form": BidForm(), 
        'totalBids': total_bids,
        'last_bid': last_bid,
        'me': myLastBid,
        'title': Listing.objects.get(id=id),
        'my_watchlist': my_watchlist,
        "comments": Comment.objects.filter(listing = id)
    })

def categories(request):
    
    categories = {}

    for i in category_options:
        categories[i[0]] = i[1]

    return render(request, 'auctions/category.html', {
        "categories": categories
    })

def showCategories(request, category):
    auctions = Listing.objects.filter(category = category)

    return render(request, 'auctions/showCategories.html',{
        "auctions": auctions,
        'categories': categories
    })

@login_required
def bid(request, id):

    if request.method == 'POST':
        form = BidForm(request.POST)
        listingAdd = Listing.objects.get(id=id)
        if form.is_valid():
            # message for the Last bid greater than current bid

            bid = form.cleaned_data['bid']
            totalBids =  Bid.objects.filter(listing = id).count()
            
            try:
                # If it matches a record, validate and save

                if totalBids > 0:
                    last_bid = Bid.objects.filter(listing = id)[totalBids-1]
                else:
                    last_bid = Bid.objects.get(listing= id)
                    

                if last_bid.bid >= bid or listingAdd.starting_bid >= bid:
                    messages.error(request, 'The bid must be higher than the previous one')
                    return redirect('listing', id=id)

                    
                bidCreate = Bid.objects.create(listing=listingAdd, bid=bid, bidder=request.user)
                bidCreate.save()
                listingAdd.bids.add(bidCreate)

            except:
                # Otherwise save the entry
                
                if listingAdd.starting_bid >= bid:
                    messages.error(request, 'The first bid must be higher than the initial bid')
                    return redirect('listing', id=id)

                bidCreate = Bid.objects.create(listing=listingAdd, bid=bid, bidder=request.user)
                bidCreate.save()
                listingAdd.bids.add(bidCreate)


    return redirect('listing', id=id)

@login_required
def create_list(request):
    
    if request.method == 'POST':
        form = CreateListForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.save()
            messages.success(request, 'Product added successfully')
            return redirect('index')

    else:
        form = CreateListForm()


    return render(request, 'auctions/createList.html', {
        'form': form
        })

@login_required
def closeList(request, id):
    if request.method == "GET":
        listing = Listing.objects.get(id = id)
        listing.active = False
        listing.save()
        return redirect('listing', id=id)

@login_required
def showWatchlist(request):
    
    my_watchlist = Watchlist.objects.get(user= request.user)
    
    return render(request, 'auctions/watchlist.html', {
        'my_watchlist': my_watchlist
    })

@login_required
def saveWatchlist(request, listing_id):

    watchlist = Watchlist.objects.get(user = request.user)

    listingAdd = Listing.objects.get(id = listing_id)

    watchlist.listings.add(listingAdd)

    return redirect('listing', listing_id)

@login_required
def watchlistRemove(request, listing_id):

    watchlist = Watchlist.objects.get(user = request.user)
    listingRemove = Listing.objects.get(id = listing_id)

    watchlist.listings.remove(listingRemove)
    
    return redirect('show-watchlist')

def comment(request, id):
    if request.method == 'POST':
        auction = Listing.objects.get(id = id)
        comment = request.POST['comment']
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            if not comment:
                return render('listing', id=id)
            else:
                commentCreate = Comment.objects.create(user = request.user, listing= auction, comment = comment )
                commentCreate.save()
                return redirect('listing', id=id)

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
            watchlist = Watchlist.objects.create(user=user)
            watchlist.save()
            user.save()

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
