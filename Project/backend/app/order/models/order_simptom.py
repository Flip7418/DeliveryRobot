from django.db import models
from django.db.models import CASCADE

from order.models.order import Order
from pill.models import Simptom


class OrderSimptom(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE,
                              related_name='order_simptoms')
    simptom = models.ForeignKey(Simptom, on_delete=CASCADE)

    class Meta:
        app_label = "order"
        verbose_name = "Order simptom"
        verbose_name_plural = "Order simptoms"

    def __str__(self):
        return f"{str(self.order)} -> {str(self.simptom)}"
