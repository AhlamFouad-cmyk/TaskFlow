from django.urls import path
from .views import SignUpView

urlpatterns = [
    # Page d'inscription
    path("signup/", SignUpView.as_view(), name="signup"),
]
