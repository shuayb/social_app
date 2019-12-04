from django.urls import path
from .views import (TweetListByUserAPIView,
                    TweetLikeAPIView,
                    TweetCreateAPIView,
                    TweetDetailAPIView,
                    TweetFeedListAPIView,
                    TweetRetweetAPIView, TweetReplyAPIView)

app_name = 'tweet'

urlpatterns = [
    path('', TweetCreateAPIView.as_view(), name='create'),

    path('feed/', TweetFeedListAPIView.as_view(), name='feed-list'),
    path('user/<int:user_pk>/', TweetListByUserAPIView.as_view(), name='list'),

    path('<int:tweet_pk>/', TweetDetailAPIView.as_view(), name='detail'),
    path('<int:tweet_pk>/like/', TweetLikeAPIView.as_view(), name='like'),
    path('<int:tweet_pk>/retweet/', TweetRetweetAPIView.as_view(), name='retweet'),
    path('<int:tweet_pk>/reply/', TweetReplyAPIView.as_view(), name='reply'),

]
