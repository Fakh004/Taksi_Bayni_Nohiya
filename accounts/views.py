from django.shortcuts import render,redirect,HttpResponse
from .models import CustomUser
from django.contrib.auth import login,logout,authenticate


def register_view(request):
    if request.method == "GET":
        return render(request,'accounts/register.html')
    elif request.method == "POST":
        username = request.POST.get('username',None)
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        confirm = request.POST.get('confirm',None)

        if not username or not email or not password:
            return render(request,'accounts/register.html',context={'username':username,"email":email,'error':'All fields are required!'})
        
        if password != confirm:
            return render(request,'accounts/register.html',context={'username':username,'error':"Passwords don't match!"})
        
        CustomUser.objects.create_user(username=username,email=email,password=password)


        return HttpResponse('Logined')



def login_view(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html')
    
    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not username or not password:
            return render(request, 'accounts/login.html', context={
                'username': username,
                'error': 'All fields are required!'
            })
        
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("driver_list")

        return render(request, 'accounts/login.html', context={
            'username': username,
            'error': "Such user does not exist!"
        })
    


def logout_confirm(request):
    return render(request, "accounts/logout_confirm.html")
