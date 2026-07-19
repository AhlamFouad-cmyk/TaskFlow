from django.contrib.auth import get_user_model
from django.test import TestCase


# ==========================================================
# Tests de création des utilisateurs
# ==========================================================

class UsersManagersTests(TestCase):

    # Vérifie la création d'un utilisateur
    def test_create_user(self):

        User = get_user_model()

        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass1234",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    # Vérifie la création d'un superutilisateur
    def test_create_superuser(self):

        User = get_user_model()

        admin_user = User.objects.create_superuser(
            username="testsuperuser",
            email="testsuperuser@example.com",
            password="testpass1234",
        )

        self.assertEqual(admin_user.username, "testsuperuser")
        self.assertEqual(admin_user.email, "testsuperuser@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
