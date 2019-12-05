from django.db import models
from django.db.models import SET_NULL, CASCADE
from rest_framework.reverse import reverse

from social_app.settings import AUTH_USER_MODEL
from tweet.managers import TweetManager


class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=SET_NULL, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, null=False, on_delete=CASCADE)
    content = models.CharField(max_length=240)
    liked = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='liked_tweets')
    reply = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("tweet:detail", kwargs={"pk": self.pk})

    def get_parent(self):
        the_parent = self
        if self.parent:
            the_parent = self.parent
        return the_parent

    def get_children(self):
        parent = self.get_parent()
        qs = Tweet.objects.filter(parent=parent)
        qs_parent = Tweet.objects.filter(pk=parent.pk)
        return qs | qs_parent

    objects = TweetManager()

    class Meta:
        ordering = ['-timestamp']

