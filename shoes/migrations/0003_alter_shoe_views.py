# Generated by Django 4.2.1 on 2023-05-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0002_size_remove_shoe_size_shoe_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoe',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
