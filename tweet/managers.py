from django.db.models import Manager
from django.utils import timezone as d_tz


class TweetManager(Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        qs = self.get_queryset().filter(
            user=user, parent=og_parent
        ).filter(
            timestamp__year=d_tz.now().year,
            timestamp__month=d_tz.now().month,
            timestamp__day=d_tz.now().day,
            reply=False,
        )
        if qs.exists():
            return None

        obj = self.model(
            parent=parent_obj,
            user=user,
            content=parent_obj.content,
        )
        obj.save()
        return obj

    def like_toggle(self, user, tweet_obj):
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)
        return is_liked