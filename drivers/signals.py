from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profiles

User = get_user_model()  # получаем CustomUser динамически

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(
            user=instance,
            bio="",
            experience_years=0,
            languages_spoken=""
        )
