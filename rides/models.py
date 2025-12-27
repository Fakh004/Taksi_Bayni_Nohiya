from django.db import models
from drivers.models import Drivers
from accounts.models import CustomUser as User

# Create your models here. rides 

class Rides(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    driver = models.ForeignKey(Drivers, on_delete=models.CASCADE)  
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance_km = models.FloatField()
    price = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.driver.name}"

class Payments(models.Model):
    ride_id = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)