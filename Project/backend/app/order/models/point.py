from django.db import models

from order.constants import PointTypes


class Point(models.Model):
    point_type = models.CharField(choices=PointTypes, max_length=64)
    title = models.CharField(max_length=256, default='Точка')
    longitude = models.IntegerField()
    latitude = models.IntegerField()

    class Meta:
        app_label = "order"
        verbose_name = "Point"
        verbose_name_plural = "Points"

    def __str__(self):
        return f"{self.title}"
