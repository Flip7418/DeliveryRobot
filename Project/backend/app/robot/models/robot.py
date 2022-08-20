from django.db import models


class Robot(models.Model):
    title = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)

    class Meta:
        app_label = "robot"
        verbose_name = "Robot"
        verbose_name_plural = "Robots"

    def __str__(self):
        return f"{str(self.title)} -> {str(self.is_available)}  -> " \
               f"{str(self.is_active)}"
