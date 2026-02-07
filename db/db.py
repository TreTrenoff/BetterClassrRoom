import os
from django.apps import AppConfig

class DbConfig(AppConfig):
    name = "db"                     # chemin réel
    label = "BetterClassRoom"       # nom interne utilisé par Django
    verbose_name = "BetterClassRoom"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "BetterClassRoom.sqlite3"),
    }
}