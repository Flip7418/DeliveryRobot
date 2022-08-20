from django.urls import path

from authorization.api.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login")
]
