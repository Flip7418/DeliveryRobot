import time
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, sdu_id, password, **extra_fields):
        if not sdu_id:
            raise ValueError("The sdu id must be set")

        user = self.model(sdu_id=sdu_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, sdu_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(sdu_id, password, **extra_fields)

    def create_superuser(self, sdu_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(sdu_id, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    sdu_id = models.CharField(max_length=128, unique=True)
    iin = models.CharField(max_length=52, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_student = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "sdu_id"
    REQUIRED_FIELDS = ["iin"]

    class Meta:
        app_label = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def token(self):
        dt = datetime.now() + timedelta(days=3)
        token = jwt.encode({
            'sdu_id': self.sdu_id,
            'exp': int(time.mktime(dt.timetuple()))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token
