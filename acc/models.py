import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse

from acc.managers import UserManager
from social_app.settings import STATIC_URL, DEFAULT_AVATAR_PATH, AUTH_USER_MODEL


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
    bio = models.CharField(max_length=160, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)
    following = models.ManyToManyField(AUTH_USER_MODEL,
                                       through='UserFollowingBridge',
                                       through_fields=('from_user', 'to_user'),
                                       related_name='followers')

    def get_avatar_file_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "{}.{}".format(uuid.uuid4().hex, ext)
        return os.path.join('user_avatars', filename)

    # avatar = models.ImageField(upload_to=get_avatar_file_path, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_avatar_file_path, blank=True, null=True)

    # Todo: Use field to save the count in future
    @property
    def total_following(self):
        return self.following.count()

    @property
    def total_followers(self):
        return self.followers.count()

    @property
    def absolute_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '{}{}'.format(STATIC_URL, DEFAULT_AVATAR_PATH)

    def get_absolute_url(self):
        return reverse('core:user-profile', args=[str(self.username)])

    # for Email Login
    USERNAME_FIELD = 'email'
    # remove email from REQUIRED_FIELDS
    REQUIRED_FIELDS = []
    first_name = None
    last_name = None

    def save(self, *args, **kwargs):
        # Check save if adding via
        # Todo Delete previous image file if updating
        # if not self._state.adding:
        #     old_instance = User.objects.get(pk=self.pk)
        #     if old_instance.avatar:
        #         if self.avatar != old_instance.avatar:
        #             old_instance.avatar.delete(False)
        super().save(*args, **kwargs)

    objects = UserManager()

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

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("Can't follow self.")