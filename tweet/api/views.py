from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from tweet.models import Tweet

from .pagination import StandardResultsPagination
from .serializers import TweetModelSerializer


class TweetLikeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        is_liked = Tweet.objects.like_toggle(request.user,
                                             get_object_or_404(Tweet, pk=self.kwargs.get('tweet_pk')))
        return Response({'liked': is_liked})


class TweetRetweetAPIView(APIView):
    def post(self, request, *args, **kwargs):
        new_tweet = Tweet.objects.retweet(request.user,
                                          get_object_or_404(Tweet, pk=self.kwargs.get('tweet_pk')))
        if new_tweet is not None:
            data = TweetModelSerializer(new_tweet).data
            return Response(data)
        return Response({"message": "Error Occurred"},
                        status=400)


class TweetCreateAPIView(CreateAPIView):
    serializer_class = TweetModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetReplyAPIView(TweetCreateAPIView):
    pass


class TweetDetailAPIView(ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        tweet_obj = get_object_or_404(Tweet, pk=self.kwargs.get('tweet_pk'))
        qs = tweet_obj.get_children()
        qs = qs.distinct()
        return qs


class TweetListByUserAPIView(ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        requested_user = self.kwargs.get("user_pk")
        if requested_user:
            return Tweet.objects.filter(user_id=requested_user)
        raise ParseError


class TweetFeedListAPIView(ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        followed_users = self.request.user.following.all()
        qs1 = Tweet.objects.filter(user__in=followed_users)
        qs2 = Tweet.objects.filter(user=self.request.user)
        qs = (qs1 | qs2).distinct()
        return qs
