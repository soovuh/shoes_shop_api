from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoes = models.ManyToManyField('shoes.Shoe', through='CartItem')
    last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.email} Cart'

    def update_last_modified(self):
        self.last_modified = timezone.now()
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoe = models.ForeignKey('shoes.Shoe', on_delete=models.CASCADE)
    user_size = models.IntegerField()
    user_qty = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_last_modified()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_last_modified()

    def __str__(self):
        return self.shoe.name
