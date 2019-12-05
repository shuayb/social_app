from django.utils.timesince import timesince

from acc.api.serializers import UserDetailSerializer, UserMiniSerializer
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from post.models import Post, Comment


class CommentSerializer(ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    date_display = SerializerMethodField()
    timesince = SerializerMethodField()
    # likes = SerializerMethodField()
    # did_like = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            # 'likes',
            # 'did_like',
            'user'
        ]

    # def get_did_like(self, obj):
    #     try:
    #         user = self.context.get('request').user
    #         if user in obj.liked.all():
    #             return True
    #     except AttributeError:
    #         pass
    #     return False

    # def get_likes(self, obj):
    #     return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def create(self, validated_data):
        comment = Comment(
            content=validated_data['content'],
            user=validated_data['user'],
            post=Post.objects.get(id=validated_data['post_pk'])
        )
        comment.save()
        return comment


class PostModelSerializer(ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    date_display = SerializerMethodField()
    timesince = SerializerMethodField()
    likes = SerializerMethodField()
    did_like = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'likes',
            'did_like',
            'attached_image'
        ]
        # read_only_fields = ['reply']

    def get_did_like(self, obj):
        try:
            user = self.context.get('request').user
            if user in obj.liked.all():
                return True
        except AttributeError:
            pass
        return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class PostCommentsModelSerializer(PostModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostModelSerializer.Meta):
        fields = PostModelSerializer.Meta.fields + ['comments']
