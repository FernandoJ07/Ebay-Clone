from collections import namedtuple
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createList", views.create_list, name='create-list'),
    path('listing/<int:id>', views.listing, name='listing'),
    path('saveWatchlist/<int:listing_id>', views.saveWatchlist, name="watchlist"),
    path('watchlist', views.showWatchlist, name='show-watchlist'),
    path('watchlistRemove/<int:listing_id>', views.watchlistRemove, name="watchlistRemove"),
    path('bid/<int:id>', views.bid, name='bid'),
    path('close/<int:id>', views.closeList, name='close-list' ),
    path('comment/<int:id>', views.comment, name='comment'),
    path('categories', views.categories, name="categories"),
    path('showCategories/<int:category>', views.showCategories, name='showCategories')
]
