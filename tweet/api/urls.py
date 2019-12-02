from django.conf.urls import url
from django.urls import path
from django.views.generic.base import RedirectView

from .views import (
    # LikeToggleAPIView,
    # RetweetAPIView,
    # TweetCreateAPIView,
    TweetListAPIView,
    # TweetDetailAPIView
)

app_name = 'tweet'


urlpatterns = [

    path('user/<int:user_pk>/', TweetListAPIView.as_view(), name='list'),

    # url(r'^create/$', TweetCreateAPIView.as_view(), name='create'),
    # url(r'^(?P<pk>\d+)/$', TweetDetailAPIView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like_toggle'),
    # url(r'^(?P<pk>\d+)/retweet/$', RetweetAPIView.as_view(), name='retweet'),
]
