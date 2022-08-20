from django.db import models
from django.db.models import CASCADE, DO_NOTHING

from order.constants import OrderTypes, OrderStatuses, OrderModerationType
from order.models.point import Point
from student.models import Student


class Order(models.Model):
    order_type = models.CharField(choices=OrderTypes, max_length=64)
    student = models.ForeignKey(Student, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    on_destination_time = models.DateTimeField(null=True, blank=True)
    destination = models.ForeignKey(Point, on_delete=DO_NOTHING, null=True,
                                    blank=True, default=1)
    status = models.CharField(choices=OrderStatuses, max_length=128,
                              default=OrderModerationType)
    description = models.TextField(null=True, blank=True)

    pills = models.ManyToManyField('pill.Pill', through='order.OrderPill',
                                   related_name='orders')
    simptoms = models.ManyToManyField('pill.Simptom',
                                      through='order.OrderSimptom',
                                      related_name='orders')

    class Meta:
        app_label = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"{str(self.student)} -> {self.order_type}"
