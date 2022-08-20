from django.db import models
from django.db.models import CASCADE

from pill.models import Simptom


class Pill(models.Model):
    title = models.CharField(max_length=256, unique=True)
    photo = models.ImageField(null=True, blank=True)
    description = models.TextField()

    class Meta:
        app_label = "pill"
        verbose_name = "Pill"
        verbose_name_plural = "Pills"

    def __str__(self):
        return self.title


class SimptomPill(models.Model):
    pill = models.ForeignKey(Pill, on_delete=CASCADE)
    simptom = models.ForeignKey(Simptom, on_delete=CASCADE)

    class Meta:
        app_label = "pill"
        verbose_name = "Simptom pill"
        verbose_name_plural = "Simptom pills"

    def __str__(self):
        return f"{str(self.simptom)} -> {str(self.pill)}"
