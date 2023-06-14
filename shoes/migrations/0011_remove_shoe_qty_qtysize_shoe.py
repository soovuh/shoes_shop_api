# Generated by Django 4.2.1 on 2023-06-12 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0010_homepagecarousel_sequence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoe',
            name='qty',
        ),
        migrations.AddField(
            model_name='qtysize',
            name='shoe',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='shoes.shoe'),
            preserve_default=False,
        ),
    ]