from django.db.models.signals import post_save
from django.conf import settings
from .models import Profile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Double-check: only create if one doesn't already exist (paranoia mode)
        Profile.objects.get_or_create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

# Manual signal registration (clean & explicit)
post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(save_user_profile, sender=settings.AUTH_USER_MODEL)
