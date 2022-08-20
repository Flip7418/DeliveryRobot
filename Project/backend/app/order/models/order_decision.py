from django.db import models
from django.db.models import CASCADE

from doctor.models import Doctor
from order.models import Order
from pill.models import Pill


class OrderDecision(models.Model):
    order = models.OneToOneField(Order, on_delete=CASCADE,
                                 related_name='order_decision')
    doctor = models.ForeignKey(Doctor, on_delete=CASCADE)
    decline_reason = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        app_label = "order"
        verbose_name = "Order decision"
        verbose_name_plural = "Order decisions"

    def __str__(self):
        return f"{str(self.order)} -> {str(self.doctor)}"


class OrderDecisionPill(models.Model):
    order_decision = models.ForeignKey(OrderDecision, on_delete=CASCADE,
                                       related_name='pills')
    pill = models.ForeignKey(Pill, on_delete=CASCADE, related_name='decision')
    count = models.IntegerField(default=1)

    class Meta:
        app_label = "order"
        verbose_name = "Order decision pill"
        verbose_name_plural = "Order decision pills"

    def __str__(self):
        return f"{str(self.order_decision)} -> {str(self.pill)}  -> " \
               f"{str(self.count)}"
