# Generated by Django 2.2.7 on 2019-12-04 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='liked',
        ),
    ]
