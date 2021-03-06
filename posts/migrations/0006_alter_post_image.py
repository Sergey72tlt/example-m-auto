# Generated by Django 4.0.3 on 2022-05-16 14:09

import django.core.validators
from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=posts.models.user_post_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg'])]),
        ),
    ]
