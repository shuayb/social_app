from django.utils.timesince import timesince
from rest_framework import serializers

from acc.api.serializers import UserDetailSerializer, UserMiniSerializer
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

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


class ParentSerializer(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


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
            'attached_image',
            # 'parent'
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

    def to_representation(self, obj):
        # Add any self-referencing fields here (if not already done)
        if 'parent' not in self.fields:
            self.fields['parent'] = PostModelSerializer(obj)
        return super().to_representation(obj)


class PostCommentsModelSerializer(PostModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostModelSerializer.Meta):
        fields = PostModelSerializer.Meta.fields + ['comments']



