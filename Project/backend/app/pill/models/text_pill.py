from django.db import models
from pill.models import Pill
from django.db.models import CASCADE


class Text(models.Model):
    pill = models.OneToOneField(Pill, on_delete=CASCADE, related_name='text')
    pharmacotherapeutic_group = models.TextField(default=" ")
    description = models.TextField(default=" ")
    indication = models.TextField(default=" ")
    application_method = models.TextField(default=" ")

    class Meta:
        app_label = "pill"
        verbose_name = "Text"
        verbose_name_plural = "Texts"

    def __str__(self):
        return self.pharmacotherapeutic_group