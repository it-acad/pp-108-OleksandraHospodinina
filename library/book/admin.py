from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'count', 'order')

    search_fields = ('name', 'description', 'order__username')

    list_filter = ('count', 'order')

    list_editable = ('name', 'count')

    fieldsets = (
        ('Book Information', {
            'fields': ('name', 'description', 'count'),
            'description': 'Information about the book that doesn\'t change.',
        }),
        ('Order Information', {
            'fields': ('order',),
            'description': 'Information about who borrowed the book.',
        }),
    )