# Generated by Django 4.0.3 on 2022-04-06 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancel_reason',
            field=models.TextField(blank=True),
        ),
    ]