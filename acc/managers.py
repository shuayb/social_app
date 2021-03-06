from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager
from django.db.models import Manager, QuerySet, Count, F, CharField, Value as V
from django.db.models.functions import Concat
from social_app.settings import MEDIA_URL


class CustomUserManager(UserManager):

    def following_top(self, user):
        qs_following = user.following.all()
        qs = (qs_following
              .annotate(x=Count('tweet'), y=Count('post'))
              .order_by('-x', '-y'))

        # qs = (user
        #       .following
        #       .annotate(Count('tweet'), Count('post'))
        #       .order_by('tweet', 'post'))

        # user.following.annotate(Count('tweet'), Count('post')).order_by('tweet', 'post').distinct('tweet')
        #      .values('id', 'username', 'avatar'))
        return qs

    def followers_top(self, user):
        qs_following = user.followers.all()
        qs = (qs_following.
              annotate(x=Count('tweet'), y=Count('post'))
              .order_by('-x', '-y'))

        #  (user
        #   .followers
        # .annotate(Count('tweet'), Count('post'),
        #           absolute_avatar_url=Concat(
        #               V(MEDIA_URL + '/'), 'avatar', output_field=CharField())
        #           )
        # .annotate(Count('tweet'), Count('post'))
        # .order_by('tweet', 'post'))
        # .values('id', 'username', 'absolute_avatar_url'))

        return qs

    def is_following(self, user, other_user):
        if other_user in user.following.all():
            return True
        else:
            return False

    def toggle_follow(self, user, to_toggle_user):
        if to_toggle_user in user.following.all():
            user.following.remove(to_toggle_user)
            added = False
        else:
            user.following.add(to_toggle_user)
            added = True
        return added