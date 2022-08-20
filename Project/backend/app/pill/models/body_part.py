from django.db import models


class BodyPart(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        app_label = "pill"
        verbose_name = "Body part"
        verbose_name_plural = "Body parts"

    def __str__(self):
        return self.title
