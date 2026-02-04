import os
from django.conf import settings
from db.db import DATABASES

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="dev-key",
        ROOT_URLCONF="urls",
        AUTH_USER_MODEL='db.User',
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'db',
        ],
        MIDDLEWARE=[],
        DATABASES=DATABASES,
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [BASE_DIR],
            }
        ],
    )