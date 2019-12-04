from django.urls import path
from tweet.views import NewTweet, TweetDetailView, reply_tweet_modal

app_name = 'tweet'

urlpatterns = [
    path('new/', NewTweet.as_view(), name='new-tweet-partial'),
    path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
    path('tweet-reply/<int:tweet_pk>/', reply_tweet_modal, name='reply-tweet')
]
