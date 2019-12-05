"""social_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_js_reverse.views import urls_js
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from social_app import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path('docs/', get_swagger_view(title='Social App API Docs'), name='api-docs'),

    # App Core
    path('', include('core.urls', namespace='core')),
    path('account/', include('acc.urls', namespace='acc')),
    path('tweets/', include('tweet.urls', namespace='tweet')),
    path('posts/', include('post.urls', namespace='post')),

    # APIs
    path('api/v1/account/', include('acc.api.urls', namespace='api-acc')),
    path('api/v1/tweets/', include('tweet.api.urls', namespace='api-tweet')),
    path('api/v1/posts/', include('post.api.urls', namespace='api-post')),

    # url(r'^api/tweet/', include('tweets.api.urls', namespace='tweet-api')),

    # JS Path
    path('url-js-list/', urls_js, name='js_reverse'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)