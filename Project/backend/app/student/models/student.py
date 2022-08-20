from django.db import models

from user.models.user import User


class Student(models.Model):
    SPECIALIZATION_CHOICES = (
        ("cs", "Computer Science"),
        ("is", "Internet Security")
    )

    allergy = models.CharField(max_length=2048, null=True, blank=True)
    specialization = models.CharField(choices=SPECIALIZATION_CHOICES,
                                      max_length=128)

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

    class Meta:
        app_label = "student"
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return str(self.user)
