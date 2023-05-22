from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Shoe, QtySize, Brand


@admin.register(Shoe)
class ShoeAdmin(ModelAdmin):
    pass


@admin.register(QtySize)
class SizeAdmin(ModelAdmin):
    pass


@admin.register(Brand)
class SizeAdmin(ModelAdmin):
    pass
