from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser, Address


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'name', 'phone_number', 'address', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Contact Information', {'fields': ('phone_number', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password', 'is_staff',
                'is_active', 'groups', 'user_permissions',
                'phone_number', 'address'
            )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
