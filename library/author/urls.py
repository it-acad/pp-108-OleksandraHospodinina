from django.urls import path
from .views import show_all_authors, create_author, delete_author

urlpatterns = [
    path('', show_all_authors, name='show_all_authors'),
    path('create/', create_author, name='create_author'),
    path('delete/<int:author_id>/', delete_author, name='delete_author'),
]
