# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.verification_token:
            self.verification_token = get_random_string(64)
        super().save(*args, **kwargs)

