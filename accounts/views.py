from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .models import CustomUser

def register_view(request):
    if request.method == "GET":
        return render(request, 'accounts/register.html')

    elif request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm = request.POST.get('confirm', '').strip()

        if not username or not email or not password:
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'error': 'All fields are required!'
            })

        if password != confirm:
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'error': "Passwords don't match!"
            })

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'username': username,
                'error': 'Username already taken!'
            })

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        login(request, user)  
        return redirect('driver_list')


def login_view(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html')

    elif request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(request, 'accounts/login.html', {
                'username': username,
                'error': 'All fields are required!'
            })

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('driver_list')

        return render(request, 'accounts/login.html', {
            'username': username,
            'error': "Incorrect username or password!"
        })

def logout_confirm_view(request):
    return render(request, "accounts/logout_confirm.html")

def logout_view(request):
    logout(request)
    return redirect('driver_list')