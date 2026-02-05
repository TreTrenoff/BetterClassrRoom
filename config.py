import os
from django.conf import settings
from db.db import DATABASES  # Configuration de ta base de données

# -------------------------------------------------------------------
# Répertoire de base du projet
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------------
# Configuration Django
# -------------------------------------------------------------------
if not settings.configured:
    settings.configure(
        # ---- DEBUG ----
        DEBUG=True,  # Mode développement (True pour debug, False en prod)

        # ---- Clé secrète ----
        SECRET_KEY="dev-key",  # Changer en production !

        # ---- Hôtes autorisés ----
        ALLOWED_HOSTS=["*"],  # Dév local uniquement

        # ---- URLs ----
        ROOT_URLCONF="urls",

        # ---- Applications installées ----
        INSTALLED_APPS=[
            "django.contrib.auth",           # Gestion des utilisateurs
            "django.contrib.contenttypes",   # Types de contenu
            "django.contrib.sessions",       # Sessions et cookies
            "django.contrib.messages",       # Messages flash
            "django.contrib.staticfiles",    # Fichiers statiques
            "db",                            # Ton application perso
        ],

        # ---- Middleware ----
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ],

        # ---- Base de données ----
        DATABASES=DATABASES,  # Import depuis db/db.py

        # ---- Templates ----
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [os.path.join(BASE_DIR, "html")],  # Répertoire des templates
                "APP_DIRS": True,  # Recherche aussi dans les apps
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            }
        ],

        # ---- Fichiers média (uploads) ----
        MEDIA_ROOT=os.path.join(BASE_DIR, "media"),  # Où sont stockés les fichiers uploadés
        MEDIA_URL="/media/",  # URL publique pour y accéder

        # ---- Fichiers statiques (CSS, JS, images) ----
        STATIC_URL="/static/",
        STATICFILES_DIRS=[
            os.path.join(BASE_DIR, "static"),  # Où mettre les fichiers statiques custom (ex: default_avatar.png)
        ],
        STATIC_ROOT=os.path.join(BASE_DIR, "staticfiles"),  # Collectstatic place ici tous les fichiers
    )
