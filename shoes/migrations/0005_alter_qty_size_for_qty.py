# Generated by Django 4.2.1 on 2023-05-21 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0004_qty_remove_shoe_qty_shoe_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qty',
            name='size_for_qty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoes.size'),
        ),
    ]
