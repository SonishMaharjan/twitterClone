from django.conf.urls import url
from .views import TweetListAPIView


app_name="tweets-api"


urlpatterns=[
    url(r'^$',TweetListAPIView.as_view(),name="list"),

]