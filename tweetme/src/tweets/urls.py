
from django.conf.urls import url

from .views import tweet_detail_view,tweet_list_view,tweet_create_view
from .views import TweetDetailView,TweetListView,TweetCreateView,TweetUpdateView,TweetDeleteView,RetweetView
from django.views.generic.base import RedirectView

app_name="tweets"

urlpatterns = [

    #function views
    #url(r'^$',tweet_list_view,name="list_view"),
    #url(r'^(?P<pok>\d+)/$',tweet_detail_view,name="detail_view"),
    #url(r'^create/$',tweet_create_view,name="create_view"),
    #class views
    #<pk> is stored in kwargs in DetailView
    url(r'^$',RedirectView.as_view(url="/")),
    url(r'^(?P<pk>\d+)/$',TweetDetailView.as_view(),name="detail_view"),
    url(r'^(?P<pk>\d+)/retweet/$',RetweetView.as_view(),name="retweet_view"),
    url(r'^search$',TweetListView.as_view(),name="list_view"),
    url(r'^create',TweetCreateView.as_view(),name="create_view"),
    url(r'^(?P<pk>\d+)/update/$',TweetUpdateView.as_view(),name="update_view"),
    url(r'^(?P<pk>\d+)/delete/$',TweetDeleteView.as_view(),name= "delete_view"),
]
