from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.http import HttpResponseForbidden
from .models import Order
from book.models import Book


@login_required
def show_all_orders(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access denied. Only admins can view all orders.")

    orders = Order.objects.all()
    return render(request, 'order/all_orders.html', {'orders': orders})


@login_required
def show_my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def create_order(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            plated_end_at = now() + timedelta(weeks=2)
            order = Order.create(user=request.user, book=book, plated_end_at=plated_end_at)
            if order:
                messages.success(request, "Order created successfully!")
                return redirect('show_my_orders')
            else:
                messages.error(request, "The book is not available for borrowing.")
        except Book.DoesNotExist:
            messages.error(request, "Book not found.")
    books = Book.objects.all()
    return render(request, 'orders/create_order.html', {'books': books})


@login_required
def close_order(request, order_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access denied. Only admins can close orders.")

    try:
        order = get_object_or_404(Order, pk=order_id)
        if not order.end_at:
            order.update(end_at=now())
            messages.success(request, f"Order {order_id} closed successfully!")
        else:
            messages.error(request, "Order is already closed.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")

    return redirect('show_all_orders')
