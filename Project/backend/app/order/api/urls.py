from django.urls import include, path
from rest_framework import routers

from order.api.views import StudentOrderViewSet, DoctorOrderViewSet

router = routers.DefaultRouter()
router.register(r"s-order", StudentOrderViewSet, basename="student orders")
router.register(r"d-order", DoctorOrderViewSet, basename="doctor orders")


urlpatterns = [
    path("", include(router.urls)),
]
