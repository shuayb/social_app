from django.urls import path
from .views import (PostCreateAPIView,
                    PostFeedListAPIView,
                    PostListByUserAPIView,
                    PostDetailAPIView,
                    PostLikeAPIView,
                    PostCommentAPIView,
                    PostShareAPIView)

app_name = 'tweet'

urlpatterns = [
    # Post Creation
    path('', PostCreateAPIView.as_view(), name='create'),

    # Latest Posts (feed) for self
    path('feed/', PostFeedListAPIView.as_view(), name='feed-list'),

    # latest Posts (specific user)
    path('user/<int:user_pk>/', PostListByUserAPIView.as_view(), name='list'),

    # Single Post with comments
    path('<int:post_pk>/', PostDetailAPIView.as_view(), name='detail'),
    path('<int:post_pk>/like/', PostLikeAPIView.as_view(), name='like'),
    path('<int:post_pk>/comment/', PostCommentAPIView.as_view(), name='comment'),
    path('<int:post_pk>/share/', PostShareAPIView.as_view(), name='share'),

    # Comments
    # path('<int:post_pk>/comments/', CommentsListAPIView.as_view(), name='comment-list'),
    # path('<int:post_pk>/comments/<int:comment_pk>/like/', CommentLikeAPIView.as_view(), name='comment-like'),

]
