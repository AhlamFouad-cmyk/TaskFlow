from multiprocessing import context

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.utils import timezone

from django.contrib import messages

from .models import Task
from .forms import TaskForm


# ==========================================================
# Page d'accueil
# ==========================================================
def home(request):
    """
    Affiche la page d'accueil de l'application.
    """
    return render(request, "home.html")


# ==========================================================
# Page À propos
#
# Cette vue affiche une page présentant l'application
# TaskFlow et ses principales fonctionnalités.
# ==========================================================

def about(request):
    return render(request, "about.html")


# ==========================================================
# Liste des tâches
#
# Fonctionnalités :
# - Affiche uniquement les tâches de l'utilisateur connecté.
# - Recherche par titre.
# - Filtre par statut.
# - Envoie les statistiques au tableau de bord.
# ==========================================================
class TaskListView(LoginRequiredMixin, ListView):

    # Modèle utilisé
    model = Task

    # Template affiché
    template_name = "tasks/task_list.html"

    # Nom de la variable envoyée au template
    context_object_name = "tasks"

    # ------------------------------------------------------
    # Liste des tâches
    # ------------------------------------------------------
    def get_queryset(self):

        queryset = Task.objects.filter(
            author=self.request.user
        ).order_by("-created_at")

        # Recherche
        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        # Filtre par statut
        status = self.request.GET.get("status")

        if status:
            queryset = queryset.filter(
                status=status
            )

        # Filtre par priorité
        priority = self.request.GET.get("priority")

        if priority:
            queryset = queryset.filter(
                priority=priority
            )
        return queryset

    # ------------------------------------------------------
    # Statistiques du tableau de bord
    # ------------------------------------------------------
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(
            author=self.request.user
        )

        # Nombre total
        context["total_tasks"] = tasks.count()

        # Nombre de tâches à faire
        context["todo_tasks"] = tasks.filter(
            status="TODO"
        ).count()

        # Nombre de tâches en cours
        context["progress_tasks"] = tasks.filter(
            status="IN_PROGRESS"
        ).count()

        # Nombre de tâches terminées
        context["done_tasks"] = tasks.filter(
            status="DONE"
        ).count()

        # Pourcentage de progression
        if context["total_tasks"] > 0:
            context["progress_percent"] = int(
                (context["done_tasks"] / context["total_tasks"]) * 100
            )
        else:
            context["progress_percent"] = 0

        context["today"] = timezone.now().date()

        return context


# ==========================================================
# Création d'une tâche
# ==========================================================
class TaskCreateView(LoginRequiredMixin, CreateView):

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    # Associer automatiquement la tâche
    # à l'utilisateur connecté.
    def form_valid(self, form):

        form.instance.author = self.request.user

        messages.success(
            self.request,
            "✅ La tâche a été créée avec succès."
        )
        return super().form_valid(form)


# ==========================================================
# Modification d'une tâche
# ==========================================================
class TaskUpdateView(LoginRequiredMixin, UpdateView):

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    # L'utilisateur ne peut modifier
    # que ses propres tâches.
    def get_queryset(self):

        return Task.objects.filter(
            author=self.request.user
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            "✏️ La tâche a été modifiée avec succès."
        )
        return super().form_valid(form)


# ==========================================================
# Vue permettant d'afficher le détail d'une tâche
#
# DetailView :
#   Affiche toutes les informations d'un seul objet.
#
# Sécurité :
#   L'utilisateur ne peut consulter que ses propres tâches.
# ==========================================================

class TaskDetailView(LoginRequiredMixin, DetailView):

    # Modèle utilisé
    model = Task

    # Template affiché
    template_name = "tasks/task_detail.html"

    # Nom de l'objet envoyé au template
    context_object_name = "task"

    # Sécurité : uniquement les tâches de l'utilisateur connecté
    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

# ==========================================================
# Suppression d'une tâche
# ==========================================================


class TaskDeleteView(LoginRequiredMixin, DeleteView):

    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    # L'utilisateur ne peut supprimer
    # que ses propres tâches.
    def get_queryset(self):

        return Task.objects.filter(
            author=self.request.user
        )

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "🗑️ La tâche a été supprimée avec succès."
        )

        return super().delete(request, *args, **kwargs)


# ==========================================================
# Marquer une tâche comme terminée
# ==========================================================
def complete_task(request, pk):
    """
    Change directement le statut d'une tâche
    en 'DONE'.
    """

    task = get_object_or_404(
        Task,
        pk=pk,
        author=request.user
    )

    task.status = "DONE"

    task.save()

    messages.success(
        request,
        "✅ La tâche a été marquée comme terminée."
    )

    return redirect("task_list")
