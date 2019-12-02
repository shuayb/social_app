from django.urls import path
from acc import views

app_name = 'acc'

urlpatterns = [

    path('', views.ToProfile.as_view(), name='root'),
    path('update-profile/', views.UpdateProfile.as_view(), name='update-profile'),

    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('sign-up/', views.Register.as_view(), name='register'),

    # User detail profile in core.urls
]
