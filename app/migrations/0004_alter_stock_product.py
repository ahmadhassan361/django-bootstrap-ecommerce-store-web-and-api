# Generated by Django 3.2.5 on 2022-03-30 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
    ]
