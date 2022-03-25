from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.db import models


class Account(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=13, blank=False, unique=True, null=True)
    gender = models.CharField(max_length=7, choices=(('male', 'Male'), ('female', 'Female')), blank=True, null=True)
    is_verified_email = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']
    objecCharFieldts = UserManager()

    def __str__(self):
        return self.username
