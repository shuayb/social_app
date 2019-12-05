from django.contrib import admin
from .models import Post, Comment


class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'timestamp', 'attached_image')

    # form = TweetModelForm
    class Meta:
        model = Post


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'content', 'timestamp')

    # form = TweetModelForm
    class Meta:
        model = Comment


admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
