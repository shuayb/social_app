from django.db.models import Manager, QuerySet, Count, F, CharField, Value as V
from django.db.models.functions import Concat

from social_app.settings import MEDIA_URL


class UserManager(Manager):

    def following_top(self, user):
        return (user
                .following
                .annotate(Count('tweet'), Count('post'),
                          absolute_avatar_url=Concat(
                              V(MEDIA_URL + '/'), 'avatar', output_field=CharField())
                          )
                .order_by('tweet', 'post')
                .values('id', 'username', 'absolute_avatar_url'))

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

    def get_by_natural_key(self, email):
        return self.get(email=email)

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email