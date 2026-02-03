import os
from django.conf import settings
from db import DATABASES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="dev-key",
        ROOT_URLCONF="urls",
        ALLOWED_HOSTS=["*"],
        MIDDLEWARE=[],
        DATABASES=DATABASES,
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [BASE_DIR],
            }
        ],
    )