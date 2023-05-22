from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class QtySize(models.Model):
    size = models.IntegerField()
    qty = models.IntegerField()

    def __str__(self):
        return f'{self.size}: {self.qty}'


class Shoe(models.Model):
    SEX_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
    )
    BRAND_CHOICES = (
        ('Nike', 'Nike'),
        ('Adidas', 'Adidas'),
        ('Kappa', 'Kappa'),
        ('Vans', 'Vans'),
        ('Puma', 'Puma'),
        ('Reebok', 'Reebok')
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
    href = models.CharField(max_length=255, default='./product.html')
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sex = models.CharField(choices=SEX_CHOICES, max_length=10)
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sale = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    views = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    qty = models.ManyToManyField(QtySize)

    def __str__(self):
        return self.name
