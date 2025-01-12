from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Author
from book.models import Book


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def show_all_authors(request):
    authors = Author.objects.all()
    return render(request, 'authors/all_authors.html', {'authors': authors})


@login_required
@user_passes_test(is_admin)
def show_author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'authors/author_detail.html', {'author': author})


@login_required
@user_passes_test(is_admin)
def create_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')

        if not name or not surname or not patronymic:
            messages.error(request, "All fields are required.")
            return redirect('create_author')

        author = Author.create(name=name, surname=surname, patronymic=patronymic)
        if author:
            messages.success(request, "Author created successfully.")
            return redirect('show_all_authors')
        else:
            messages.error(request, "Error creating the author.")
            return redirect('create_author')

    return render(request, 'authors/create_author.html')


@login_required
@user_passes_test(is_admin)
def delete_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if author.books.count() == 0:
        author.delete()
        messages.success(request, "Author deleted successfully.")
    else:
        messages.error(request, "Author is attached to books and cannot be deleted.")

    return redirect('show_all_authors')
