from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class QtySize(models.Model):
    size = models.IntegerField()
    qty = models.IntegerField()
    shoe = models.ForeignKey('Shoe', on_delete=models.CASCADE, related_name='sizes')

    def __str__(self):
        return f'{self.size}: {self.qty}'


class Shoe(models.Model):
    SEX_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
    )
    TYPE_CHOICES = (
        ('running', 'running'),
        ('retro', 'retro'),
        ('slip-on', 'slip-on'),
        ('low-top', 'low-top'),
        ('high-top', 'high-top'),
        ('skate', 'skate'),
    )

    name = models.CharField(max_length=255)
    info = models.TextField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sex = models.CharField(choices=SEX_CHOICES, max_length=10)
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sale = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    views = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HomePageCarousel(models.Model):
    image = models.ImageField(upload_to='carousel_images')
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return str(self.sequence)
