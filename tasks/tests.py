from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import Task


# ==========================================================
# Tests de la page d'accueil
# ==========================================================

class HomePageTests(SimpleTestCase):

    def test_url_exists_at_correct_location_homepage(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "home.html")

        self.assertContains(response, "Bienvenue")


# ==========================================================
# Tests de la page À propos
# ==========================================================

class AboutPageTests(SimpleTestCase):

    def test_url_exists_at_correct_location_about(self):

        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)

    def test_aboutpage_view(self):

        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "about.html")

        self.assertContains(response, "TaskFlow")


# ==========================================================
# Tests du modèle Task
# ==========================================================

class TaskModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="ahlam",
            password="test1234",
        )

        self.task = Task.objects.create(
            title="Créer TaskFlow",
            description="Projet Django",
            status="TODO",
            priority="HIGH",
            due_date="2026-07-20",
            author=self.user,
        )

    # Vérifie la création d'une tâche
    def test_create_task(self):

        self.assertEqual(self.task.title, "Créer TaskFlow")
        self.assertEqual(self.task.status, "TODO")
        self.assertEqual(self.task.priority, "HIGH")

    # Vérifie la méthode __str__()
    def test_task_string_representation(self):

        self.assertEqual(str(self.task), "Créer TaskFlow")


# ==========================================================
# Tests des vues Task
# ==========================================================

class TaskViewTests(TestCase):

    def setUp(self):

        # Création d'un utilisateur
        self.user = User.objects.create_user(
            username="ahlam",
            password="test1234",
        )

        # Connexion de l'utilisateur
        self.client.login(
            username="ahlam",
            password="test1234",
        )

        # Création d'une tâche
        self.task = Task.objects.create(
            title="Créer Dashboard",
            description="Projet Django",
            status="TODO",
            priority="HIGH",
            due_date="2026-07-20",
            author=self.user,
        )

    # ------------------------------------------------------
    # Vérifie que la liste des tâches s'affiche
    # ------------------------------------------------------

    def test_task_list_view(self):

        response = self.client.get(
            reverse("task_list")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "tasks/task_list.html",
        )

        self.assertContains(
            response,
            "Créer Dashboard",
        )

    # ------------------------------------------------------
    # Vérifie la page détail
    # ------------------------------------------------------

    def test_task_detail_view(self):

        response = self.client.get(
            reverse(
                "task_detail",
                args=[self.task.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "tasks/task_detail.html",
        )

        self.assertContains(
            response,
            "Créer Dashboard",
        )

# ==========================================================
# Tests de création, modification et suppression
# ==========================================================


class TaskCrudTests(TestCase):

    def setUp(self):

        # Création d'un utilisateur
        self.user = User.objects.create_user(
            username="ahlam",
            password="test1234",
        )

        # Connexion
        self.client.login(
            username="ahlam",
            password="test1234",
        )

        # Création d'une tâche
        self.task = Task.objects.create(
            title="Première tâche",
            description="Description",
            status="TODO",
            priority="MEDIUM",
            due_date="2026-07-20",
            author=self.user,
        )

    # ------------------------------------------------------
    # Vérifie la création d'une tâche
    # ------------------------------------------------------

    def test_create_task(self):

        response = self.client.post(
            reverse("task_create"),
            {
                "title": "Nouvelle tâche",
                "description": "Créer les tests",
                "status": "TODO",
                "priority": "HIGH",
                "due_date": "2026-07-30",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Task.objects.count(), 2)

    # ------------------------------------------------------
    # Vérifie la modification d'une tâche
    # ------------------------------------------------------

    def test_update_task(self):

        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {
                "title": "Tâche modifiée",
                "description": "Nouvelle description",
                "status": "DONE",
                "priority": "LOW",
                "due_date": "2026-07-25",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()

        self.assertEqual(self.task.title, "Tâche modifiée")
        self.assertEqual(self.task.status, "DONE")

    # ------------------------------------------------------
    # Vérifie la suppression d'une tâche
    # ------------------------------------------------------

    def test_delete_task(self):

        response = self.client.post(
            reverse("task_delete", args=[self.task.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Task.objects.count(), 0)
