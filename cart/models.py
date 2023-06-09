
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoes = models.ManyToManyField('shoes.Shoe', through='CartItem')

    def __str__(self):
        return f'{self.user.email} Cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoe = models.ForeignKey('shoes.Shoe', on_delete=models.CASCADE)
    user_size = models.IntegerField()
    user_qty = models.IntegerField()

    def __str__(self):
        return self.shoe.name
