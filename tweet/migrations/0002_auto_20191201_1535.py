# Generated by Django 2.2.7 on 2019-12-01 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='is_reply',
            new_name='reply',
        ),
    ]
