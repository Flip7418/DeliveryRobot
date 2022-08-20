from django.db import models
from django.db.models import CASCADE

from order.models.order import Order
from pill.models import Pill


class OrderPill(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE,
                              related_name='order_pills')
    pill = models.ForeignKey(Pill, on_delete=CASCADE)
    count = models.IntegerField()

    class Meta:
        app_label = "order"
        verbose_name = "Order pill"
        verbose_name_plural = "Order pills"

    def __str__(self):
        return f"{str(self.order)} -> {str(self.pill)}"
