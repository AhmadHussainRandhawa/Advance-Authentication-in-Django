from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    # superuser only needs email/password

    def __str__(self):
        return f"{self.email}"

