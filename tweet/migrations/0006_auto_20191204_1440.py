# Generated by Django 2.2.7 on 2019-12-04 10:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0005_auto_20191203_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='liked_tweets', to=settings.AUTH_USER_MODEL),
        ),
    ]
