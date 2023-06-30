from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('canceled', 'canceled'),
        ('delivered', 'delivered'),
        ('processed', 'processed'),
    )
    name = models.CharField(max_length=20, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoes = models.ManyToManyField('shoes.Shoe', through='OrderItem')
    status = models.CharField(choices=STATUS_CHOICES, max_length=55, default='processed')
    total = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    address = models.ForeignKey(to='OrderAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'№{self.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shoe = models.ForeignKey('shoes.Shoe', on_delete=models.CASCADE)
    user_size = models.IntegerField()
    user_qty = models.IntegerField()

    def __str__(self):
        return self.shoe.name


class OrderAddress(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    postcode = models.CharField(max_length=5, blank=True, default='')

    def __str__(self):
        return f'{self.city}, {self.street}, {self.postcode}'
