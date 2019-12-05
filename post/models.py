import os
import uuid

from django.db import models
from django.db.models import Model, CASCADE, Manager, SET_NULL

from post.manager import PostManager
from social_app.settings import AUTH_USER_MODEL


class Post(Model):
    parent = models.ForeignKey("self", null=True, on_delete=SET_NULL, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, null=False, on_delete=CASCADE)
    liked = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='liked_posts')
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_attached_image_file_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "{}.{}".format(uuid.uuid4().hex, ext)
        return os.path.join('user_posts', filename)

    attached_image = models.ImageField(upload_to=get_attached_image_file_path, blank=True, null=True)

    def __str__(self):
        return self.content

    objects = PostManager()

    class Meta:
        ordering = ['-timestamp']


class Comment(Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    user = models.ForeignKey(AUTH_USER_MODEL, null=False, on_delete=CASCADE)
    content = models.CharField(max_length=250, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    # objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    # Todo Nested Comments, Comments Likes
    # replies = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='comments_replies')
    # liked = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='comments_liked')
