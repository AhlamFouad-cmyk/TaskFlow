from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# ==========================================================
# Formulaire d'inscription
#
# UserCreationForm est fourni par Django.
# Il contient déjà :
# - username
# - password1
# - password2
#
# Nous allons simplement le personnaliser.
# ==========================================================

class SignUpForm(UserCreationForm):

    class Meta:

        # Modèle utilisé
        model = User

        # Champs affichés
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]
