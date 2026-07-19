from django.urls import path
from .views import (
    home,
    about,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    complete_task,
)

# creation des adresses :127.0.0.1:8000/about

urlpatterns = [
    # Accueil
    path("", home, name="home"),

    # Page À propos
    path("about/", about, name="about"),

    # Liste des tâches
    path("tasks/", TaskListView.as_view(), name="task_list"),

    # Détail d'une tâche
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail",),

    # Nouvelle tâche
    path("tasks/new/", TaskCreateView.as_view(), name="task_create"),

    # Modification
    path(
        "tasks/<int:pk>/edit/",
        TaskUpdateView.as_view(),
        name="task_update",
    ),

    # Suppression d'une tâche
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task_delete",
    ),

    # Marquer une tâche comme terminée
    path(
        "tasks/<int:pk>/complete/",
        complete_task,
        name="task_complete",
    ),

]
