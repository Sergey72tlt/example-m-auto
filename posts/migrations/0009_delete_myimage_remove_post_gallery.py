# Generated by Django 4.0.3 on 2022-05-25 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_myimage_post_gallery'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyImage',
        ),
        migrations.RemoveField(
            model_name='post',
            name='gallery',
        ),
    ]
