from django.urls import path

from doctor.api.views import ProfileViewSet

urlpatterns = [
    path('profile/', ProfileViewSet.as_view()),
]
