from django.urls import path
from acc import views

app_name = 'acc'

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]
