# Generated by Django 4.0.3 on 2022-04-04 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='country',
            new_name='province',
        ),
    ]
