"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from authentication import views as auth_views


def home_view(request):
    return HttpResponse("<h1>Welcome to the Library</h1>")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('', auth_views.home, name='home'),
    path('books/', include('book.urls')),
    path('users/', auth_views.show_all_users, name='show_all_users'),
    path('users/<int:user_id>/', auth_views.show_user_detail, name='show_user_detail'),
    path('orders/', include('order.urls')),
    path('authors/', include('author.urls')),
]
