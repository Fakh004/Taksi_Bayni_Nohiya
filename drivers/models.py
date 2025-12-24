from django.db import models

# Create your models here.

class Drivers(models.Model):
    image = models.ImageField(upload_to='driver_images/', null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    car_model = models.CharField(max_length=100)
    car_number = models.CharField(max_length=20)
    rating = models.FloatField(default=5.0)
    status = models.BooleanField(default=True)  # True for active, False for inactive
    created_at = models.DateTimeField(auto_now=True)

class Reviews(models.Model):
    ride_id = models.IntegerField()
    user_id = models.IntegerField()
    driver_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

class Profiles(models.Model):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    driver_id = models.IntegerField()
    bio = models.TextField()
    experience_years = models.IntegerField()
    languages_spoken = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
