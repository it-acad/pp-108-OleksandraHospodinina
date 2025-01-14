from django.shortcuts import render, get_object_or_404
from .models import Book
from django.contrib.auth.models import User

def books_list(request):
    books = Book.objects.all()
    return render(request, 'book/books_list.html', {'books': books})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'book/book_detail.html', {'book': book})


def books_filter(request):
    query = request.GET.get('query')
    if query:
        books = Book.objects.filter(name__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'book/books_list.html', {'books': books})

def books_by_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    books = Book.objects.filter(order=user)
    return render(request, 'books_by_user.html', {'user': user, 'books': books})

