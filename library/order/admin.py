from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'created_at', 'end_at', 'plated_end_at')

    readonly_fields = ('created_at',)

    search_fields = ('book__name', 'user__username')
    list_filter = ('created_at', 'end_at')

    fieldsets = (
        ('Order Information', {
            'fields': ('book', 'user', 'created_at', 'end_at', 'plated_end_at'),
            'description': 'Order details including book and user.',
        }),
    )
