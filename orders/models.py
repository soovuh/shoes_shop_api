from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('canceled', 'canceled'),
        ('delivered', 'delivered'),
        ('processed', 'processed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE)
    cart_items = models.ManyToManyField('cart.CartItem')
    status = models.CharField(choices=STATUS_CHOICES, max_length=55)
    total = models.IntegerField()

    def __str__(self):
        return f'{self.user.name} Order'