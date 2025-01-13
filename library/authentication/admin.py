from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active')
    ordering = ('id',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        ('Personal information', {
            'fields': ('email', 'first_name', 'last_name', 'middle_name', 'password')
        }),
        ('Roles and status', {
            'fields': ('role', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2', 'role', 'is_active'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


admin.site.register(CustomUser, CustomUserAdmin)
