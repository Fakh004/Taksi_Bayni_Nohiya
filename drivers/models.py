from django.db import models

# Create your models here.

class Drivers(models.Model):
    image = models.ImageField(upload_to='driver_images/', null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    car_model = models.CharField(max_length=100)
    car_number = models.CharField(max_length=20)
    car_photo = models.ImageField(upload_to='car_images/', null=True, blank=True)
    rating = models.FloatField(default=5.0)
    status = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name  

class Reviews(models.Model):
    ride_id = models.IntegerField()
    user_id = models.IntegerField()
    driver_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

from django.conf import settings
from django.db import models

class Profiles(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    languages_spoken = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"