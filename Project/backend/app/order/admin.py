from django.contrib import admin

from order.models import Order, OrderPill, OrderSimptom, Point, OrderDecision, \
    OrderDecisionPill


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_type', 'status')
    list_filter = ('order_type', 'status',)


@admin.register(OrderPill)
class OrderPillAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderSimptom)
class OrderSimptomAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDecision)
class OrderDecisionAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDecisionPill)
class OrderDecisionPillAdmin(admin.ModelAdmin):
    pass


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass
