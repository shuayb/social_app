from django.urls import path
from core import views

from acc.views import Profile as acc_Profile

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('about/', views.About.as_view(), name='about'),

    path('user/<slug:slug>/', acc_Profile.as_view(), name='user-profile'),
]
