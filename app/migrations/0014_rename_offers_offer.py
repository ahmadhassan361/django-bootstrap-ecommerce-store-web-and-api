# Generated by Django 4.0.3 on 2022-04-08 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_product_video_url_product_youtube_video_url_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Offers',
            new_name='Offer',
        ),
    ]
