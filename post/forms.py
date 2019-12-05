from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'content',
            'attached_image'

        ]


class CommentForm(PostForm):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]