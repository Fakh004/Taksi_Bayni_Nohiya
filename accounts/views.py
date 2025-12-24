from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        confirm = request.POST.get("confirm_password", None)
        if not username or not password or not email:
            return render(request, "register.html", {
                "username": username,
                "email": email,
                "error": "All fields are required."})
        if password != confirm:
            return render(request, "register.html", {
                "username": username,
                "email": email,
                "error": "Passwords do not match."})
        hash_password = make_password(password)
        user= User.objects.filter(username=username).first()
        if user:
            return render(request, "register.html", {
                "username": username,
                "email": email,
                "error": "Username already exists."})
        user = User(
            username=username,
            email=email,
            password=hash_password
        )
        user.save()
        return redirect("login")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("post_list")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})


def logout_view(request):
    if request.method == "GET":
        return render(request, "logout.html")
    elif request.method == "POST":
        logout(request)
        return redirect("post_list")