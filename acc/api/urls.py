from django.urls import path, re_path

from .views import RegisterAPIView,\
    LoginAPIView,\
    LogoutAPIView,\
    UserDetail #, \
    # UserList

app_name = 'acc'

urlpatterns = [

    path('user/<int:pk>/', UserDetail.as_view(), name='profile-detail'),
    # path('users/', UserList.as_view(), name='user-list'),

    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

]
