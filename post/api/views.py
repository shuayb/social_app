from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from post.api.pagination import StandardResultsPagination
from post.api.serializers import PostModelSerializer, PostCommentsModelSerializer, CommentSerializer
from post.models import Post, Comment


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostFeedListAPIView(ListAPIView):
    pagination_class = StandardResultsPagination
    serializer_class = PostModelSerializer

    def get_queryset(self, *args, **kwargs):
        followed_users = self.request.user.following.all()
        qs1 = Post.objects.filter(user__in=followed_users)
        qs2 = Post.objects.filter(user=self.request.user)
        qs = (qs1 | qs2).distinct()
        return qs


class PostListByUserAPIView(ListAPIView):
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        requested_user = self.kwargs.get("user_pk")
        if requested_user:
            return Post.objects.filter(user_id=requested_user)
        raise ParseError


class PostDetailAPIView(RetrieveAPIView):
    serializer_class = PostCommentsModelSerializer
    lookup_url_kwarg = 'post_pk'
    queryset = Post.objects.all()


class PostLikeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        is_liked = Post.objects.like_toggle(request.user,
                                            get_object_or_404(Post, pk=self.kwargs.get('post_pk')))
        return Response({'liked': is_liked})


class PostCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        # Call  serializer's create()
        serializer.save(user=self.request.user,
                        post_pk=self.kwargs.get('post_pk'))


class PostShareAPIView(APIView):
    def post(self, request, *args, **kwargs):
        new_post = Post.objects.share(request.user,
                                      get_object_or_404(Post, pk=self.kwargs.get('post_pk')))
        if new_post is not None:
            data = PostModelSerializer(new_post).data
            return Response(data)
        return Response({"message": "Error Occurred"},
                        status=400)
