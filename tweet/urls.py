from django.urls import path
from tweet import views

app_name = 'tweet'

urlpatterns = [
    path('new/', views.NewTweet.as_view(), name='new-tweet'),
]
