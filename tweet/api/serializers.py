from django.utils.timesince import timesince

from acc.api.serializers import UserDetailSerializer, UserMiniSerializer
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from tweet.models import Tweet


class ParentTweetModelSerializer(ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    date_display = SerializerMethodField()
    timesince = SerializerMethodField()
    likes = SerializerMethodField()
    did_like = SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'likes',
            'did_like',
        ]

    def get_did_like(self, obj):
        try:
            user = request.user
            if user.is_authenticated():
                if user in obj.liked.all():
                    return True
        except:
            pass
        return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class TweetModelSerializer(ModelSerializer):
    parent_id = CharField(write_only=True, required=False)
    user = UserMiniSerializer(read_only=True)
    date_display = SerializerMethodField()
    timesince = SerializerMethodField()
    parent = ParentTweetModelSerializer(read_only=True)
    likes = SerializerMethodField()
    did_like = SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'parent_id',
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'parent',
            'likes',
            'did_like',
            'reply',
        ]
        # read_only_fields = ['reply']

    def get_did_like(self, obj):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated():
                if user in obj.liked.all():
                    return True
        except:
            pass
        return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"
