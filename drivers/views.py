from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Drivers
from django.contrib.auth.decorators import login_required

def is_authenticated(request):
    return request.user.is_authenticated

def home_view(request):
    return render(request, 'drivers/home.html')

def driver_list(request):
    drivers = Drivers.objects.all()

    
    name = request.GET.get('name')
    min_rating = request.GET.get('min_rating')
    status = request.GET.get('status')

    if name:
        drivers = drivers.filter(name__icontains=name)
    if min_rating:
        try:
            drivers = drivers.filter(rating__gte=float(min_rating))
        except ValueError:
            pass
    if status in ['active', 'inactive']:
        drivers = drivers.filter(status=(status == 'active'))

    return render(request, 'drivers/drivers_list.html', {'drivers': drivers})


def driver_create(request):
    if not is_authenticated(request):
        return render(request, 'drivers/message.html', {
            'message': "🚫 You must log in to edit a driver."
        })

    if request.method == 'POST':
        driver = Drivers.objects.create(
            image=request.FILES.get('image'),
            name=request.POST.get('name'),
            phone_number=request.POST.get('phone_number'),
            car_model=request.POST.get('car_model'),
            car_number=request.POST.get('car_number'),
            car_photo=request.FILES.get('car_photo'),
            rating=request.POST.get('rating'),
            status=request.POST.get('status') == 'on'
        )
        return redirect('driver_detail', driver_id=driver.id)

    return render(request, 'drivers/driver_create.html')


def driver_detail(request, driver_id):
    driver = Drivers.objects.filter(id=driver_id).first()
    if not driver:
        return HttpResponse('Driver not found')
    return render(request, 'drivers/driver_detail.html', {'driver': driver})


def driver_update(request, driver_id):
    if not is_authenticated(request):
        return render(request, 'drivers/message.html', {
            'message': "🚫 You must log in to edit a driver."
        })

    driver = get_object_or_404(Drivers, id=driver_id)

    if request.method == 'POST':
        driver.name = request.POST.get('name')
        driver.phone_number = request.POST.get('phone_number')
        driver.car_model = request.POST.get('car_model')
        driver.car_number = request.POST.get('car_number')
        driver.car_photo = request.FILES.get('car_photo')
        driver.rating = request.POST.get('rating')
        driver.status = request.POST.get('status') == 'true'


        if request.FILES.get('image'):
            driver.image = request.FILES['image']

        driver.save()
        return redirect('driver_detail', driver_id=driver.id)

    return render(request, 'drivers/driver_update.html', {'driver': driver})


def driver_delete_view(request, driver_id):
    if not is_authenticated(request):
        return render(request, 'drivers/message.html', {
            'message': "🚫 You must log in to edit a driver."
    })

    driver = Drivers.objects.filter(id=driver_id).first()
    if not driver:
        return HttpResponse(f"Driver with id {driver_id} not found")

    if request.method == "GET":
        return render(request, "drivers/driver_delete.html", {"driver": driver})
    elif request.method == "POST":
        driver.delete()
        return redirect("driver_list")




@login_required  
def profile_view(request):
    profile = request.user.profile
    return render(request, 'drivers/profile.html', {'profile': profile})

@login_required
def profile_update(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.experience_years = request.POST.get('experience_years', 0)
        profile.languages_spoken = request.POST.get('languages_spoken', '')

        if request.FILES.get('image'): 
            profile.image = request.FILES['image']

        profile.save()
        return redirect('profile')  

    return render(request, 'drivers/profile_update.html', {'profile': profile})

