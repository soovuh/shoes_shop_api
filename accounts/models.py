from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


from .managers import CustomUserManager
from .phone_number import PhoneNumberField


class Address(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    postcode = models.CharField(max_length=5, blank=True, default='')

    def __str__(self):
        return f'{self.city}, {self.street}, {self.postcode}'


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(blank=True, unique=True)
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(_('is active'), default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


