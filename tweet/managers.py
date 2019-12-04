from django.db.models import Manager
from django.utils import timezone as d_tz


class TweetManager(Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            original_parent = parent_obj.parent
        else:
            original_parent = parent_obj

        obj = self.model(parent=original_parent,
                         user=user,
                         content=parent_obj.content)
        obj.save()
        return obj

    def like_toggle(self, user_obj, tweet_obj):
        if user_obj in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user_obj)
        else:
            is_liked = True
            tweet_obj.liked.add(user_obj)
        return is_liked
