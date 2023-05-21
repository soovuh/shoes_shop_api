# Generated by Django 4.2.1 on 2023-05-21 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eu_size', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='shoe',
            name='size',
        ),
        migrations.AddField(
            model_name='shoe',
            name='size',
            field=models.ManyToManyField(to='shoes.size'),
        ),
    ]
