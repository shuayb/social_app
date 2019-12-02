from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from social_app import settings


class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)

    email = models.EmailField(blank=False,
                              unique=True,
                              error_messages={
                                  'unique': "A user with that email is already exists."
                                  #          "registered. If you have forgotten "
                                  #          "your password, reset it."
                              })

    name = models.CharField(max_length=50, null=True)

    bio = models.CharField(max_length=160, null=True)

    location = models.CharField(max_length=30, null=True)

    website = models.URLField(max_length=100, null=True)

    following = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       through='UserFollowingBridge',
                                       through_fields=('from_user', 'to_user'),
                                       related_name='followers')

    # Todo: Use field to save the count in future
    @property
    def total_following(self):
        return self.following.count()

    @property
    def total_followers(self):
        return self.followers.count()

    # for Email Login
    USERNAME_FIELD = 'email'
    # remove email from REQUIRED_FIELDS
    REQUIRED_FIELDS = []
    first_name = None
    last_name = None

    class Meta:
        ordering = ('id',)


class UserFollowingBridge(models.Model):
    from_user = models.ForeignKey('User',
                                  on_delete=models.CASCADE,
                                  related_name='following_user')
    to_user = models.ForeignKey('User',
                                on_delete=models.CASCADE,
                                related_name='followers_user')
    date_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '({}) {} {}'.format(
            self.id,
            self.from_user_id,
            self.to_user_id)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['from_user', 'to_user'], name='unique_users'),
        ]
