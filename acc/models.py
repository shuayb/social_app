from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)

    email = models.EmailField(blank=False,
                              unique=True,
                              error_messages={
                                  'unique': "A user with that email is already exists."
                                  #          "registered. If you have forgotten "
                                  #          "your password, reset it."
                              })

    bio = models.CharField(max_length=160, null=True)

    website = models.URLField(null=True)

    # for Email Login
    USERNAME_FIELD = 'email'
    # remove email from REQUIRED_FIELDS
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('id',)