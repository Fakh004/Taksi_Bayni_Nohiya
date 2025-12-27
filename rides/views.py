from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Rides, RideBooking
from drivers.models import Drivers
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser as User



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
    if status in ['Waiting for passangers', 'completed', 'canceled']:
        rides = rides.filter(status=status)

    return render(request, "rides/rides_list.html", {"rides": rides})





def ride_create(request):
    drivers = Drivers.objects.all()
    
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        seat_number = request.POST.get('seat_number')
        start_location = request.POST.get('start_location')
        end_location = request.POST.get('end_location')
        distance_km = request.POST.get('distance_km')
        price = request.POST.get('price')
        status = request.POST.get('status')

        driver = Drivers.objects.get(id=driver_id)
        ride = Rides.objects.create(
            user=request.user,
            driver=driver,
            start_location=start_location,
            end_location=end_location,
            distance_km=distance_km,
            price=price,
            status=status
        )
        ride.seat_number = seat_number
        ride.save()
        return redirect('ride_list')
    
    context = {
        'drivers': drivers,
        'available_seats': [1,2,3,4],  
    }
    return render(request, 'rides/ride_create.html', context)





def ride_detail(request, ride_id):
    ride = Rides.objects.filter(id=ride_id).first()
    if not ride:
        return HttpResponse("Ride not found")

    return render(request, "rides/ride_detail.html", {"ride": ride})

def ride_update(request, ride_id):
    if not request.user.is_authenticated:
        return render(request, 'rides/message.html', {'message': "🚫 You must log in to edit a ride."})

    ride = get_object_or_404(Rides, id=ride_id)
    drivers = Drivers.objects.all() 
    users = User.objects.all()    

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            ride.user = get_object_or_404(User, id=user_id)

        driver_id = request.POST.get("driver_id")
        if driver_id:
            ride.driver = get_object_or_404(Drivers, id=driver_id)

        ride.start_location = request.POST.get("start_location")
        ride.end_location = request.POST.get("end_location")
        ride.distance_km = request.POST.get("distance_km")
        ride.price = request.POST.get("price")
        ride.status = request.POST.get("status")
        ride.save()

        return redirect("ride_detail", ride_id=ride.id)

    return render(request, "rides/ride_update.html", {
        "ride": ride,
        "drivers": drivers,
        "users": users,
    })


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


def book_list(request):
    bookings = RideBooking.objects.filter(user=request.user)
    return render(request, 'rides/booking_list.html', {'bookings': bookings})


def book_ride(request, ride_id):
    ride = get_object_or_404(Rides, id=ride_id)
    booked = RideBooking.objects.filter(ride=ride).values_list('seat_number', flat=True)
    all_seats = [1, 2, 3, 4]
    available_seats = [s for s in all_seats if s not in booked]

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        seat = request.POST.get("seat_number")

        if not name or not phone:
            return render(request, "rides/booking_create.html", {
                "ride": ride,
                "available_seats": available_seats,
                "error": "Name and phone are required!",
                "name": name,
                "phone": phone
            })

        if not seat:
            return render(request, "rides/booking_create.html", {
                "ride": ride,
                "available_seats": available_seats,
                "error": "Please choose a seat!",
                "name": name,
                "phone": phone
            })

        seat = int(seat)
        if seat not in available_seats:
            return render(request, "rides/booking_create.html", {
                "ride": ride,
                "available_seats": available_seats,
                "error": "This seat is already taken!",
                "name": name,
                "phone": phone
            })

        RideBooking.objects.create(
            ride=ride,
            name=name,
            phone=phone,
            seat_number=seat
        )

        return redirect("booking_list")

    return render(request, "rides/booking_create.html", {
        "ride": ride,
        "available_seats": available_seats
    })