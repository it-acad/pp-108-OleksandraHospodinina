from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'books_count')

    search_fields = ('name', 'surname')

    list_filter = ('name', 'surname')

    def books_count(self, obj):
        return obj.books.count()

    books_count.admin_order_field = 'books_count'
    books_count.short_description = 'Number of Books'

