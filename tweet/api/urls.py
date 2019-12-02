from django.conf.urls import url
from django.urls import path
from django.views.generic.base import RedirectView

from .views import (
    TweetListAPIView,
    TweetLikeAPIView
)

app_name = 'tweet'


urlpatterns = [

    path('user/<int:user_pk>/', TweetListAPIView.as_view(), name='list'),

    path('<int:tweet_pk>/like', TweetLikeAPIView.as_view(), name='like'),

]
