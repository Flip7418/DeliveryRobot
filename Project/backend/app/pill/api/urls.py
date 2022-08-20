from django.urls import path, include
from rest_framework import routers

from pill.api.views import BodyPartViewSet

router = routers.DefaultRouter()
router.register(r"body-part", BodyPartViewSet, basename="body-parts")


urlpatterns = [
    path("", include(router.urls)),
]
