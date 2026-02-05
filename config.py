import os
from django.conf import settings
from db.db import DATABASES  # Votre configuration de base de données personnalisée

# Définition du répertoire de base pour les templates et fichiers statiques
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")

# Vérifie si Django n'est pas encore configuré avant d'appeler settings.configure
if not settings.configured:
    settings.configure(
        # ---- DEBUG ----
        DEBUG=True,  # Active le mode debug pour voir les erreurs détaillées. À mettre sur False en production.

        # ---- Clé secrète ----
        SECRET_KEY="dev-key",  # Clé secrète pour le cryptage des sessions et CSRF. Changer en production.

        # ---- URLs ----
        ROOT_URLCONF="urls",  # Le module qui contient vos urls (urls.py)
        ALLOWED_HOSTS=["*"],  # Autorise toutes les adresses pour le développement local

        # ---- Applications installées ----
        INSTALLED_APPS=[
            # Gestion des utilisateurs et permissions
            'django.contrib.auth',
            'django.contrib.contenttypes',
            
            # Sessions pour login, cookies, et CSRF
            'django.contrib.sessions',  

            # Messages flash (success, error) dans les templates
            'django.contrib.messages',  

            # Gestion des fichiers statiques (CSS, JS)
            'django.contrib.staticfiles', 

            # Votre application personnelle
            'db',
        ],

        # ---- Middleware ----
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',  # Sécurité basique (headers, SSL)
            
            # Middleware essentiel pour gérer les sessions
            'django.contrib.sessions.middleware.SessionMiddleware',  

            'django.middleware.common.CommonMiddleware',  # Normalise certaines requêtes HTTP
            'django.middleware.csrf.CsrfViewMiddleware',  # Protection contre CSRF
            'django.contrib.auth.middleware.AuthenticationMiddleware',  # Login, logout
            'django.contrib.messages.middleware.MessageMiddleware',  # Messages flash
        ],

        # ---- Base de données ----
        DATABASES=DATABASES,  # Votre configuration importée de db.db

        # ---- Templates ----
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [BASE_DIR],
                "APP_DIRS": True,  # Important si tu veux utiliser des templates dans tes apps
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",  # injecte 'request' dans les templates
                        "django.contrib.auth.context_processors.auth",  # injecte 'user'
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            }
        ],


        # ---- Médias (uploads) ----
        MEDIA_ROOT=os.path.join(BASE_DIR, "media"),  # Où les fichiers uploadés sont stockés
        MEDIA_URL="/media/",  # URL publique pour accéder aux fichiers uploadés

        # ---- Static files (CSS, JS) ----
        STATIC_URL="/static/",  # <--- IMPORTANT ! Nécessaire pour django.contrib.staticfiles
        STATIC_ROOT=os.path.join(BASE_DIR, "staticfiles"),  # Où collectstatic va stocker les fichiers statiques
    )
