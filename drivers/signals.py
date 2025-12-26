# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Drivers, Profiles

# @receiver(post_save, sender=Drivers)
# def create_driver_profile(sender, instance, created, **kwargs):
#     if created:
#         Profiles.objects.create(
#             driver_id=instance.id,
#             bio="",
#             experience_years=0,
#             languages_spoken=""
#         )
