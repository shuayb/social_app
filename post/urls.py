from django.urls import path
from post.views import NewPost, PostDetailView, comment_post_modal

app_name = 'post'

urlpatterns = [
    path('new/', NewPost.as_view(), name='new-post-partial'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('<int:post_pk>/comment/', comment_post_modal, name='comment-post'),
]
