# Generated by Django 4.2.1 on 2023-06-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_cart_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
