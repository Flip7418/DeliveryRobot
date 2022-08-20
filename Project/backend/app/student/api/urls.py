from django.urls import path

from student.api.views import ProfileViewSet

urlpatterns = [
    path('profile/', ProfileViewSet.as_view()),
]
