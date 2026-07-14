from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm


# ==========================================================
# Vue d'inscription
#
# CreateView :
#   Vue générique Django permettant de créer un nouvel objet.
#
# Ici :
#   - on crée un nouvel utilisateur ;
#   - on affiche le formulaire d'inscription ;
#   - après inscription, l'utilisateur est redirigé
#     vers la page de connexion.
# ==========================================================

class SignUpView(CreateView):

    # Formulaire utilisé
    form_class = SignUpForm

    # Template affiché
    template_name = "registration/signup.html"

    # Redirection après une inscription réussie
    success_url = reverse_lazy("login")
