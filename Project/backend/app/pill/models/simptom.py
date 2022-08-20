from django.db import models
from django.db.models import CASCADE

from pill.models import BodyPart


class Simptom(models.Model):
    title = models.CharField(max_length=256, unique=True)
    body_part = models.ForeignKey(BodyPart, on_delete=CASCADE,
                                  related_name='simptoms')
    pills = models.ManyToManyField('pill.Pill', through='pill.SimptomPill',
                                   related_name='simptoms')

    class Meta:
        app_label = "pill"
        verbose_name = "Simptom"
        verbose_name_plural = "Simptoms"

    def __str__(self):
        return self.title
