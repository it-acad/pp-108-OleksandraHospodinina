from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_all_orders, name='show_all_orders'),
    path('my/', views.show_my_orders, name='show_my_orders'),
    path('create/', views.create_order, name='create_order'),
    path('close/<int:order_id>/', views.close_order, name='close_order'),
]
