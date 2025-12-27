from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Rides
from drivers.models import Drivers


def is_authenticated(request):
    return request.user.is_authenticated


def ride_list(request):
    rides = Rides.objects.all()

   
    start = request.GET.get('start_location')
    end = request.GET.get('end_location')
    status = request.GET.get('status')

    if start:
        rides = rides.filter(start_location__icontains=start)
    if end:
        rides = rides.filter(end_location__icontains=end)
    if status in ['pending', 'completed', 'canceled']:
        rides = rides.filter(status=status)

    return render(request, "rides/rides_list.html", {"rides": rides})





def ride_create(request):
    if not is_authenticated(request):
        return render(request, 'rides/message.html', {
            'message': "🚫 You must log in to create a ride."
        })

    if request.method == "GET":
        drivers = Drivers.objects.all()
        return render(request, "rides/ride_create.html", {"drivers": drivers})

    if request.method == "POST":
        driver_name = request.POST.get("driver_name")
        driver = Drivers.objects.get(name=driver_name)

        ride = Rides.objects.create(
            user=request.user,
            driver=driver,
            start_location=request.POST.get("start_location"),
            end_location=request.POST.get("end_location"),
            distance_km=request.POST.get("distance_km"),
            price=request.POST.get("price"),
            status=request.POST.get("status")
        )

        return redirect("ride_detail", ride_id=ride.id)



def ride_detail(request, ride_id):
    ride = Rides.objects.filter(id=ride_id).first()
    if not ride:
        return HttpResponse("Ride not found")

    return render(request, "rides/ride_detail.html", {"ride": ride})


def ride_update(request, ride_id):
    if not is_authenticated(request):
        return render(request, 'rides/message.html', {
            'message': "🚫 You must log in to edit a ride."
        })

    ride = Rides.objects.filter(id=ride_id).first()
    if not ride:
        return HttpResponse("Ride not found")

    if request.method == "GET":
        return render(request, "rides/ride_update.html", {"ride": ride})

    elif request.method == "POST":
        ride.user_id = request.POST.get("user_id")
        ride.driver_id = request.POST.get("driver_id")
        ride.start_location = request.POST.get("start_location")
        ride.end_location = request.POST.get("end_location")
        ride.distance_km = request.POST.get("distance_km")
        ride.price = request.POST.get("price")
        ride.status = request.POST.get("status")
        ride.save()

        return redirect("ride_detail", ride_id=ride.id)


def ride_delete(request, ride_id):
    if not is_authenticated(request):
        return render(request, 'rides/message.html', {
            'message': "🚫 You must log in to delete a ride."
        })

    ride = Rides.objects.filter(id=ride_id).first()
    if not ride:
        return HttpResponse(f"Ride with id {ride_id} not found")

    if request.method == "GET":
        return render(request, "rides/ride_delete.html", {"ride": ride})

    elif request.method == "POST":
        ride.delete()
        return redirect("ride_list")
