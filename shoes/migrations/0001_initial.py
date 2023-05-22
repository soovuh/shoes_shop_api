# Generated by Django 4.2.1 on 2023-05-19 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField()),
                ('href', models.CharField(default='./product.html', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='item_images')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('size', models.JSONField()),
                ('sex', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=10)),
                ('type', models.CharField(choices=[('running', 'running'), ('retro', 'retro'), ('slip-on', 'slip-on'), ('low-top', 'low-top'), ('high-top', 'high-top'), ('platform', 'platform'), ('skate', 'skate'), ('classic', 'classic'), ('leather', 'leather')], max_length=50)),
                ('brand', models.CharField(choices=[('Nike', 'Nike'), ('Adidas', 'Adidas'), ('Kappa', 'Kappa'), ('Vans', 'Vans'), ('Puma', 'Puma'), ('Reebok', 'Reebok')], max_length=50)),
                ('sale', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('views', models.IntegerField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('qty', models.JSONField()),
            ],
        ),
    ]