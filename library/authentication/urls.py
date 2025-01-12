from django.urls import path
from authentication import views as auth_views
from book import views as book_views

urlpatterns = [
    path('', auth_views.home, name='home'),
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('base/', auth_views.base_view, name='base'),
    path('books/', book_views.books_list, name='books_list'),
    path('users/', auth_views.show_all_users, name='all_users'),
    path('users/<int:user_id>/', auth_views.show_user_detail, name='user_detail'),
]
