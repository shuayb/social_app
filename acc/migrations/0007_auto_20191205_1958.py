# Generated by Django 2.2.8 on 2019-12-05 15:58

import acc.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0006_auto_20191205_1429'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', acc.managers.CustomUserManager()),
            ],
        ),
    ]
