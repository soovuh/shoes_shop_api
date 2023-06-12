from django.contrib.admin import ModelAdmin

from .models import Shoe, QtySize, Brand, HomePageCarousel
from django import forms
from django.contrib import admin

from django.forms.models import BaseInlineFormSet


class QtySizeForm(forms.ModelForm):
    class Meta:
        model = QtySize
        fields = ['size', 'qty']

class QtySizeInlineFormSet(BaseInlineFormSet):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.shoe = form.instance
            instance.save()
        formset.save_m2m()

class QtySizeInline(admin.TabularInline):
    model = QtySize
    form = QtySizeForm
    formset = QtySizeInlineFormSet
    extra = 1

@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    inlines = [QtySizeInline]


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    pass


@admin.register(HomePageCarousel)
class CarouselAdmin(ModelAdmin):
    pass
