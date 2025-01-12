from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path('filter/', views.books_filter, name='books_filter'),
    path('user/<int:user_id>/', views.books_by_user, name='books_by_user'),

]
