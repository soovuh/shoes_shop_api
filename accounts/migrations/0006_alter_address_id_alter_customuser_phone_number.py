# Generated by Django 4.2.1 on 2023-06-08 15:09

import accounts.phone_number
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_address_alter_customuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=accounts.phone_number.PhoneNumberField(blank=True, max_length=20, unique=True),
        ),
    ]