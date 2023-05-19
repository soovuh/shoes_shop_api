from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Shoe


@admin.register(Shoe)
class ShoeAdmin(ModelAdmin):
    pass
