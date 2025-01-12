from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from authentication.models import CustomUser


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        role = request.POST.get('role', 0)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'authentication/register.html')

        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            role=role,
            password=password
        )

        user.is_active = True
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'authentication/login.html')

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


def base_view(request):
    return render(request, 'authentication/base.html')


def home(request):
    return render(request, 'authentication/home.html')


@login_required
def show_all_users(request):
    if request.user.role != 1:
        return HttpResponseForbidden("Access denied. You must be a librarian.")

    users = CustomUser.objects.all()
    return render(request, 'authentication/all_users.html', {'users': users})


@login_required
def show_user_detail(request, user_id):
    if request.user.role != 1:
        return HttpResponseForbidden("Access denied. You must be a librarian.")

    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'authentication/user_detail.html', {'user': user})
