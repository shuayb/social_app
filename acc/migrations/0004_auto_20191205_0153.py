# Generated by Django 2.2.7 on 2019-12-04 21:53

import acc.models
import cropperjs.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0003_auto_20191204_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to=acc.models.User.get_avatar_file_path),
        ),
    ]
