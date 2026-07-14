from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Administration
    path("admin/", admin.site.urls),

    # Application des tâches
    path("", include("tasks.urls")),

    # Authentification Django (login, logout, password...)
    path("accounts/", include("django.contrib.auth.urls")),

    # Application accounts (signup)
    path("accounts/", include("accounts.urls")),
]
