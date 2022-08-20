from django.db import models

from user.models.user import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

    class Meta:
        app_label = "doctor"
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return str(self.user)
