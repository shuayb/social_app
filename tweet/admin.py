from django.contrib import admin
from tweet.models import Tweet


class TweetModelAdmin(admin.ModelAdmin):
    list_display = ('parent', 'user', 'content', 'reply', 'updated', 'timestamp')

    # form = TweetModelForm
    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetModelAdmin)