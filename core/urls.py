from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
]
